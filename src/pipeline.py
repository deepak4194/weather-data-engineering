import logging

import pandas as pd

from ingestion.weather_api import load_cities, get_weather
from snowflake.load_weather import load_weather_records
from validation.validate_weather import validate_weather_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Starting weather pipeline...")

    try:
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

        logger.info(
            f"Collected {len(all_weather_records)} weather records"
        )

        weather_df = pd.DataFrame(all_weather_records)

        validation_errors = validate_weather_data(weather_df)

        if validation_errors:
            for error in validation_errors:
                logger.error(error)

            raise ValueError("Weather data validation failed.")

        logger.info("Weather data validation passed")

        load_weather_records(all_weather_records)

        logger.info("Weather pipeline completed successfully!")

    except Exception:
        logger.exception("Weather pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()