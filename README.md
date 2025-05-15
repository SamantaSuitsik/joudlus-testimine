# Photoprism rakenduse jõudlustestimine

Selles repositooriumis on Tartu Ülikooli tudengi lõputöö raames valminud skriptid ning testide tulemused.

Töös võrreldi omavahel Raspberry Pi'd ning ja Azure'i virtuaalmasinat. 
Töö eesmärk oli välja selgitada, milline neist on parem lahendus väikese kasutajate arvu ning suuremate andmemahtudega tegeleva rakenduse (siin Photoprismi) majutamiseks.
Üheks osaks tööst oli läbiviia jõudlustestid, et mõõta taristute võimsust.

## Jõudlustestid

Jõudlustestide läbiviimiseks kasutati skripti nimega `scenarios.py`. Skript eeldab, et eksisteerib fail piltideNimed.json, mille abil saab see kätte failid, mida hakatakse Photoprismi üleslaadima.

Skripti jooksutamiseks kasutati käsku
`locust -f scenarios.py --logfile locust.log`

Seejärel saab testi käivitada kasutajaliideses, mille leiab aadressilt
`http://localhost:8089/`
## Bashi skriptid

1. `leiaPiltideNimed.sh` skripti kasutati selleks, et leida kõikide pildifailide nimed, mis asuvad kaustas nimega "pildid". Skript eeldab kausta "pildid" olemasolu.
2. Suurtel hulgal failide liigutamiseks üheks kaustast teise kasutati skripti `teisaldaKasutatudPildid.sh`. See eeldab, et on olemas logifail nimega "locust.log", mille põhjal faile teisaldama hakatakse.

## Locusti testide aruanded

Kaust "Locusti testide aruanded", sisaldab Locusti testi lõppedes genereeritud aruandeid, milles on näha erinevate päringute täitmise ajad. Nende aruannete põhjal hinnati Raspberry Pi ja virtuaalmasina jõudlust.
