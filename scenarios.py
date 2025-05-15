import os
import json
import random
import string
import logging

from locust import HttpUser, task, between, LoadTestShape, TaskSet


logging.basicConfig(filename='locust.log', filemode='w', level=logging.INFO)


def generate_upload_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


with open("piltideNimed.json") as files_json:
    file_list = json.load(files_json)


class UserTasks(TaskSet):
    def get_some_photo_uid(self):
        url = "/api/v1/photos?count=120&offset=0&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=newest&q=&public=true"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    random_index = random.randrange(len(response_data) - 1)
                    return response_data[random_index]["UID"]

                except Exception as e:
                    response.failure("UID parsimine ebaõnnestus: " + str(e))

    def show_all_photos(self):
        url = "/api/v1/photos?count=120&offset=0&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=newest&q=&public=true"
        self.client.get(url)

    def filter_gray_photos(self):
        url = "/api/v1/photos?count=120&offset=0&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=grey&order=newest&q=&public=true"
        self.client.get(url)

    def upload_file(self, upload_id):
        file_name = random.choice(file_list)
        logging.info("Photo: %s", file_name)
        file_path = os.path.join("./pildid", file_name)

        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"files": (file_name, file_content, "image/jpeg")}

        url = f"/api/v1/users/ustwjk273i6ivct8/upload/{upload_id}"
        with self.client.post(url, files=files, catch_response=True) as res:
            if res.status_code != 200:
                res.failure("POST-päring ebaõnnestus pildi üleslaadimisel!")

        put_payload = {"albums": []}
        with self.client.put(url, data=json.dumps(put_payload), catch_response=True) as put_res:
            if put_res.status_code != 200:
                put_res.failure("PUT-päring ebaõnnestus pildi üleslaadimisel!")

    def download_photo(self, uid):
        url = f"/api/v1/photos/{uid}/dl"
        self.client.get(url)


class UploadScenario(UserTasks):
    @task
    def scenario(self):
        upload_id = generate_upload_id()

        self.show_all_photos()
        self.upload_file(upload_id)


class ViewScenario(UserTasks):
    @task
    def scenario(self):
        self.show_all_photos()
        self.filter_gray_photos()


class DownloadScenario(UserTasks):
    @task
    def scenario(self):
        uid = self.get_some_photo_uid()

        self.download_photo(uid)


class PhotoprismUser(HttpUser):
    wait_time = between(1, 1)
    tasks = [ViewScenario]  # default scenario

    scenario_sequence = [
        UploadScenario,
        ViewScenario,
        DownloadScenario,
        ViewScenario,
        DownloadScenario,
    ]

    def __init__(self, parent):
        super().__init__(parent)
        # figure out which “slot” this user is
        idx = self.environment.runner.user_count - 1
        chosen = self.scenario_sequence[idx % len(self.scenario_sequence)]
        # override at instance level with a list of one TaskSet
        self.tasks = [chosen]

