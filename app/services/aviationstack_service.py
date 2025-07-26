import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIVATION_STACK_API_KEY", "NOT FOUND")
BASE_URL = "https://api.aviationstack.com/v1/flights"
OUTPUT_FOLDER = "app/output"

def get_output_filename(date: str):
    return f"{OUTPUT_FOLDER}/flights_{date}_00-00_to_07-00.json"

async def get_flight_data(date: str):
    file_path = get_output_filename(date)
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    if os.path.exists(file_path):
        print("using cached data")
        with open(file_path, "r") as f:
            return json.load(f)

    params = {
        "access_key": API_KEY,
        "date": date
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json().get("data", [])

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return data
