#!/bin/bash
files=()
while IFS= read -r file; do
  files+=("\"$(basename "$file")\"")
done < <(find ./pildid -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))
echo "["$(IFS=,; echo "${files[*]}")"]" > piltideNimed.json
