import logging

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

from .connection import get_snowflake_connection

logger = logging.getLogger(__name__)

def load_weather_records(weather_records):
    if not weather_records:
        logger.warning("No weather records to load.")
        return

    connection = get_snowflake_connection()
    cursor = connection.cursor()

    try:
        dataframe = pd.DataFrame(weather_records)

        dataframe.columns = [
            "CITY",
            "WEATHER_TIME",
            "TEMPERATURE",
            "HUMIDITY",
            "PRESSURE",
            "WIND_SPEED",
            "WEATHER_CODE",
            "PRECIPITATION"
        ]

        cursor.execute("""
            CREATE TEMPORARY TABLE WEATHER_LOAD_TEMP (
                CITY VARCHAR,
                WEATHER_TIME TIMESTAMP_NTZ,
                TEMPERATURE FLOAT,
                HUMIDITY FLOAT,
                PRESSURE FLOAT,
                WIND_SPEED FLOAT,
                WEATHER_CODE INTEGER,
                PRECIPITATION FLOAT
            )
        """)

        success, _, rows_loaded, _ = write_pandas(
            connection,
            dataframe,
            "WEATHER_LOAD_TEMP",
            auto_create_table=False
        )

        if not success:
            raise RuntimeError("Failed to bulk load weather data.")

        logger.info(
    f"Bulk loaded {rows_loaded} records into temporary table"
)

        merge_query = """
            MERGE INTO WEATHER_DB.RAW.WEATHER_RAW AS target
            USING WEATHER_LOAD_TEMP AS source
            ON target.CITY = source.CITY
               AND target.WEATHER_TIME = source.WEATHER_TIME

            WHEN NOT MATCHED THEN
                INSERT (
                    CITY,
                    WEATHER_TIME,
                    TEMPERATURE,
                    HUMIDITY,
                    PRESSURE,
                    WIND_SPEED,
                    WEATHER_CODE,
                    PRECIPITATION
                )
                VALUES (
                    source.CITY,
                    source.WEATHER_TIME,
                    source.TEMPERATURE,
                    source.HUMIDITY,
                    source.PRESSURE,
                    source.WIND_SPEED,
                    source.WEATHER_CODE,
                    source.PRECIPITATION
                )
        """

        cursor.execute(merge_query)
        connection.commit()

        logger.info(
    f"Processed {len(weather_records)} weather records"
)

    finally:
        cursor.close()
        connection.close()