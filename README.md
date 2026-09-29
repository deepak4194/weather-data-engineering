# 🌦️ Weather Data Engineering Pipeline

An end-to-end weather data engineering pipeline built using Python, Open-Meteo, and Snowflake.

## Architecture

Open-Meteo API
↓
Python Ingestion
↓
Snowflake RAW
↓
Stream
↓
Task
↓
STAGING
↓
Dynamic Table
↓
Analytics
↓
Dashboard

## Technologies

- Python
- Open-Meteo API
- Snowflake
- Snowflake Streams
- Snowflake Tasks
- Snowflake Dynamic Tables
- Pandas
- PyArrow
- Git

## Data Flow

### 1. Data Ingestion

Weather data is retrieved from Open-Meteo for:

- Hyderabad
- Vijayawada
- Chennai
- Bengaluru
- Mumbai
- Delhi

Hourly weather observations are collected for each city.

### 2. RAW Layer

The Python pipeline loads the weather observations into:

`WEATHER_DB.RAW.WEATHER_RAW`

The loader uses bulk loading and a duplicate-safe `MERGE`.

### 3. CDC Layer

A Snowflake Stream tracks changes to the RAW table.

### 4. STAGING Layer

A Snowflake Task processes new records from the Stream and loads them into:

`WEATHER_DB.STAGING.WEATHER_STAGING`

### 5. Analytics Layer

A Dynamic Table provides the analytics-ready dataset:

`WEATHER_DB.ANALYTICS.WEATHER_ANALYTICS_DT`

The Dynamic Table currently has a target lag of 1 hour.

## Current Status

- Python API ingestion: Complete
- Snowflake connection: Complete
- RAW layer: Complete
- Stream: Complete
- Task: Complete
- STAGING layer: Complete
- Dynamic Table: Complete
- Analytics views: Complete
- Python → Snowflake pipeline: Complete
- Logging: Complete
- Error handling: Complete