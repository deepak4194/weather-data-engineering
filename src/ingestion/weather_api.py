import json
import logging
import time

import requests


API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES_FILE = "config/cities.json"

logger = logging.getLogger(__name__)


def load_cities():
    """Load city configuration from cities.json."""
    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_weather(city, latitude, longitude, max_retries=3):
    """Fetch weather data for a city with retry handling."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "pressure_msl,"
            "wind_speed_10m,"
            "weather_code,"
            "precipitation"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    for attempt in range(1, max_retries + 1):

        try:
            logger.info(
                f"Fetching weather for {city} "
                f"(attempt {attempt}/{max_retries})"
            )

            response = requests.get(
                API_URL,
                params=params,
                timeout=(10, 60)
            )

            logger.info(
                f"Weather API response for {city}: "
                f"HTTP {response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            hourly = data.get("hourly")

            if not hourly:
                raise ValueError(
                    f"No hourly weather data returned for {city}"
                )

            weather_records = []

            for i in range(len(hourly["time"])):

                weather_records.append({
                    "city": city,
                    "weather_time": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "humidity": hourly["relative_humidity_2m"][i],
                    "pressure": hourly["pressure_msl"][i],
                    "wind_speed": hourly["wind_speed_10m"][i],
                    "weather_code": hourly["weather_code"][i],
                    "precipitation": hourly["precipitation"][i]
                })

            logger.info(
                f"Successfully collected "
                f"{len(weather_records)} records for {city}"
            )

            return weather_records

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ) as error:

            logger.warning(
                f"Network error for {city} "
                f"(attempt {attempt}/{max_retries}): {error}"
            )

            if attempt < max_retries:
                wait_time = attempt * 5

                logger.info(
                    f"Retrying {city} in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                logger.error(
                    f"Failed to fetch weather for {city} "
                    f"after {max_retries} attempts."
                )

        except requests.exceptions.RequestException as error:

            logger.error(
                f"Weather API request failed for {city}: {error}"
            )

            if attempt < max_retries:
                wait_time = attempt * 5
                time.sleep(wait_time)
            else:
                raise

        except Exception:
            logger.exception(
                f"Unexpected error while processing {city}"
            )
            raise

    # Important:
    # Returning an empty list allows the pipeline to continue
    # processing other cities when a temporary API failure occurs.
    return []


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    cities = load_cities()

    all_weather_records = []

    for city in cities:

        records = get_weather(
            city["city"],
            city["latitude"],
            city["longitude"]
        )

        all_weather_records.extend(records)

    logger.info(
        f"Total weather records collected: "
        f"{len(all_weather_records)}"
    )
