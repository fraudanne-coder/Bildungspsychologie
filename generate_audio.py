import csv
import os
import requests

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "6V1EWbNGUufEsfPFe5VA"
CSV_FILE = "bildungspsychologie.csv"
OUTPUT_DIR = "audio"

os.makedirs(OUTPUT_DIR, exist_ok=True)

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

with open(CSV_FILE, mode="r", encoding="utf-8-sig") as file:
    sample = file.read(1024)
    file.seek(0)
    delimiter = ";" if ";" in sample else ","
    reader = csv.reader(file, delimiter=delimiter)

    for index, row in enumerate(reader, start=1):
        if len(row) < 2 or not row[1].strip():
            continue

        text = row[1].strip()
        output_path = os.path.join(OUTPUT_DIR, f"{index}.mp3")

        if os.path.exists(output_path):
            print(f"Übersprungen (existiert bereits): {output_path}")
            continue

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.65,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, "wb") as audio_file:
                audio_file.write(response.content)
            print(f"Erstellt: {output_path} -> '{row[0].strip()}'")
        else:
            print(f"Fehler bei Zeile {index}: {response.status_code} - {response.text}")
