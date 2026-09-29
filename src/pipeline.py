import logging


from ingestion.weather_api import load_cities, get_weather
from snowflake.load_weather import load_weather_records

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

        load_weather_records(all_weather_records)

        logger.info("Weather pipeline completed successfully!")

    except Exception:
        logger.exception("Weather pipeline failed")
        raise

    
if __name__ == "__main__":
    run_pipeline()