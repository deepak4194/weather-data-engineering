import json
import logging
import csv
import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"

def load_cities():
    with open("config/cities.json", "r") as file:
        cities = json.load(file)

    return cities

def save_to_csv(weather_records, file_path):
    if not weather_records:
        print("No weather records to save.")
        return

    fieldnames = [
        "city",
        "weather_time",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "weather_code",
        "precipitation"
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(weather_records)

    print(f"Saved {len(weather_records)} records to {file_path}")

def get_weather(city, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "wind_speed_10m",
            "weather_code",
            "precipitation"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(API_URL, params=params)

    logger.info(
    f"Weather API response for {city}: HTTP {response.status_code}"
)

    response.raise_for_status()

    data = response.json()

    hourly_data = data["hourly"]

    times = hourly_data["time"]
    temperatures = hourly_data["temperature_2m"]
    humidities = hourly_data["relative_humidity_2m"]
    pressures = hourly_data["pressure_msl"]
    wind_speeds = hourly_data["wind_speed_10m"]
    weather_codes = hourly_data["weather_code"]
    precipitations = hourly_data["precipitation"]

    weather_records = []

    for i in range(len(times)):
        record = {
            "city": city,
            "weather_time": times[i],
            "temperature": temperatures[i],
            "humidity": humidities[i],
            "pressure": pressures[i],
            "wind_speed": wind_speeds[i],
            "weather_code": weather_codes[i],
            "precipitation": precipitations[i]
        }

        weather_records.append(record)

    return weather_records


if __name__ == "__main__":
    cities = load_cities()

    all_weather_records = []

    for city in cities:
        city_name = city["city"]
        latitude = city["latitude"]
        longitude = city["longitude"]

        weather_records = get_weather(
            city_name,
            latitude,
            longitude
        )

        all_weather_records.extend(weather_records)

    print(f"\nTotal weather records collected: {len(all_weather_records)}")

    print("\nFirst 5 records:")

    for record in all_weather_records[:5]:
        print(record)

    save_to_csv(
        all_weather_records,
        "data/weather_data.csv"
    )