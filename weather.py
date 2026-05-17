import os
import requests
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "weather.csv"


def fetch_weather(api_key: str, city="Moscow") -> dict:
    if not api_key:
        raise ValueError("API_KEY is not found. Check your .env file.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    weather_data = response.json()

    return weather_data

def parse_weather_data(weather_data: dict) -> dict:
    weather = weather_data["weather"][0]
    main = weather_data["main"]
    wind = weather_data["wind"]

    timestamp = weather_data["dt"]
    timezone_offset = weather_data.get("timezone", 0)
    city_timezone = timezone(timedelta(seconds=timezone_offset))
    readable_datetime = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).astimezone(city_timezone)


    row = {
        "datetime": readable_datetime.isoformat(),
        "city": weather_data["name"],
        "weather_main": weather["main"],
        "weather_description": weather["description"],
        "temp": main["temp"],
        "feels_like": main["feels_like"],
        "pressure": main["pressure"],
        "wind_speed": wind["speed"],
    }

    return row


def save_weather_to_csv() -> None:
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)    

    row = parse_weather_data(data)

    fieldnames = [
        "datetime",
        "city",
        "weather_main",
        "weather_description",
        "temp",
        "feels_like",
        "pressure",
        "wind_speed",
    ]

    file_is_empty = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0


    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file_is_empty:
            writer.writeheader()

        writer.writerow(row)


if __name__ == "__main__":
    # test weather API
    save_weather_to_csv()
