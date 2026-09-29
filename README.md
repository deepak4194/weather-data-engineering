# 🌦️ Weather Data Engineering Pipeline

An end-to-end **data engineering project** that collects weather forecast data from the **Open-Meteo API**, processes and validates it using **Python**, loads it into **Snowflake**, performs incremental processing with **Streams and Tasks**, transforms it using a **Dynamic Table**, exposes analytics through **Snowflake Views**, and presents the results through an interactive **Streamlit dashboard**.

The entire ingestion workflow is automated using **GitHub Actions**, which runs the pipeline daily.

> **Project Type:** End-to-End Data Engineering / Cloud Data Pipeline  
> **Primary Technologies:** Python, Snowflake, Open-Meteo, GitHub Actions, Streamlit  
> **Current Cities:** Hyderabad, Vijayawada, Chennai, Bengaluru, Mumbai, Delhi, Kolkata, Pune  
> **Automation:** Daily at 06:00 AM IST  
> **Dashboard:** Deployed using Streamlit Community Cloud

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Architecture](#-architecture)
- [End-to-End Data Flow](#-end-to-end-data-flow)
- [Core Data Engineering Concepts](#-core-data-engineering-concepts)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Source](#-data-source)
- [Python Ingestion Pipeline](#-python-ingestion-pipeline)
- [Data Validation](#-data-validation)
- [Snowflake Architecture](#-snowflake-architecture)
- [RAW Layer](#-raw-layer)
- [Streams](#-streams)
- [Tasks](#-tasks)
- [STAGING Layer](#-staging-layer)
- [Dynamic Tables](#-dynamic-tables)
- [Analytics Layer](#-analytics-layer)
- [Streamlit Dashboard](#-streamlit-dashboard)
- [Automation with GitHub Actions](#-automation-with-github-actions)
- [Security and Secrets Management](#-security-and-secrets-management)
- [Deployment](#-deployment)
- [Adding a New City](#-adding-a-new-city)
- [Local Setup](#-local-setup)
- [Running the Pipeline](#-running-the-pipeline)
- [Key Engineering Decisions](#-key-engineering-decisions)
- [What This Project Demonstrates](#-what-this-project-demonstrates)
- [Future Improvements](#-future-improvements)
- [Conclusion](#-conclusion)

---

# 🚀 Project Overview

Weather data is generated continuously and can be useful for analytics, monitoring, planning, and decision-making.

This project demonstrates how raw data from an external API can be transformed into a complete cloud-based data pipeline.

The pipeline:

1. Retrieves weather forecast data from Open-Meteo.
2. Loads city configuration dynamically from a JSON file.
3. Collects weather observations using Python.
4. Validates the collected dataset.
5. Loads the data into Snowflake RAW.
6. Uses a Snowflake Stream to capture changes.
7. Uses a Snowflake Task for incremental processing.
8. Stores transformed records in the STAGING layer.
9. Uses a Snowflake Dynamic Table to maintain the analytics dataset.
10. Creates analytical views for reporting.
11. Displays the results through a Streamlit dashboard.
12. Automates daily ingestion through GitHub Actions.
13. Deploys the dashboard using Streamlit Community Cloud.

The project is designed to demonstrate a realistic **API → Cloud Data Warehouse → Transformation → Analytics → Dashboard** workflow.

---

# 🎯 Problem Statement

Weather APIs provide useful data, but consuming an API directly from an application does not demonstrate a complete data engineering workflow.

The goal of this project is to build a pipeline that can:

- Collect weather data from an external API.
- Process and validate the incoming data.
- Store raw data in a cloud data warehouse.
- Incrementally process new data.
- Transform the data into analytics-ready structures.
- Provide reusable analytical datasets.
- Automate data ingestion.
- Present the processed information through an interactive dashboard.

---

# 🎯 Project Objectives

The main objectives are:

- Build an end-to-end data pipeline using Python and Snowflake.
- Integrate an external REST API.
- Implement configuration-driven ingestion.
- Apply data quality validation.
- Separate raw, staging, and analytics layers.
- Use Snowflake Streams for change tracking.
- Use Snowflake Tasks for automated processing.
- Use Snowflake Dynamic Tables for derived analytical data.
- Create reusable analytics views.
- Build an interactive Streamlit dashboard.
- Automate the pipeline using GitHub Actions.
- Deploy the dashboard to Streamlit Community Cloud.
- Implement secure credential management.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │    Open-Meteo API   │
                         │  Weather Forecasts  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Python Ingestion   │
                         │                     │
                         │ • API Requests      │
                         │ • Configuration     │
                         │ • Transformation    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Data Validation   │
                         │                     │
                         │ • Schema checks     │
                         │ • Null checks       │
                         │ • City checks       │
                         │ • Duplicate checks  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────┐
                    │           SNOWFLAKE              │
                    │                                  │
                    │  ┌────────────────────────────┐  │
                    │  │            RAW             │  │
                    │  │        WEATHER_RAW         │  │
                    │  └──────────────┬─────────────┘  │
                    │                 │                │
                    │                 ▼                │
                    │  ┌────────────────────────────┐  │
                    │  │           STREAM           │  │
                    │  │     WEATHER_RAW_STREAM     │  │
                    │  └──────────────┬─────────────┘  │
                    │                 │                │
                    │                 ▼                │
                    │  ┌────────────────────────────┐  │
                    │  │            TASK            │  │
                    │  │   LOAD_WEATHER_STAGING     │  │
                    │  └──────────────┬─────────────┘  │
                    │                 │                │
                    │                 ▼                │
                    │  ┌────────────────────────────┐  │
                    │  │          STAGING           │  │
                    │  │       WEATHER_STAGING      │  │
                    │  └──────────────┬─────────────┘  │
                    │                 │                │
                    │                 ▼                │
                    │  ┌────────────────────────────┐  │
                    │  │       DYNAMIC TABLE        │  │
                    │  │     WEATHER_ANALYTICS_DT   │  │
                    │  └──────────────┬─────────────┘  │
                    │                 │                │
                    │                 ▼                │
                    │  ┌────────────────────────────┐  │
                    │  │       ANALYTICS VIEWS      │  │
                    │  │                            │  │
                    │  │ • CITY_WEATHER_SUMMARY     │  │
                    │  │ • DAILY_WEATHER_SUMMARY    │  │
                    │  │ • LATEST_WEATHER           │  │
                    │  └──────────────┬─────────────┘  │
                    └─────────────────┼────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────┐
                         │ Streamlit Dashboard │
                         │                     │
                         │ • KPIs              │
                         │ • City comparison   │
                         │ • Trends            │
                         │ • Latest weather    │
                         │ • Daily summaries   │
                         └─────────────────────┘


             ┌──────────────────────────────────────────┐
             │            GitHub Actions                │
             │                                          │
             │       Daily at 06:00 AM IST              │
             │                  │                       │
             │                  ▼                       │
             │          python src/pipeline.py          │
             └──────────────────────────────────────────┘
```

---

# 🔄 End-to-End Data Flow

```text
Open-Meteo
    ↓
cities.json
    ↓
Python API ingestion
    ↓
Pandas DataFrame
    ↓
Data validation
    ↓
Snowflake RAW
    ↓
Snowflake Stream
    ↓
Snowflake Task
    ↓
Snowflake STAGING
    ↓
Dynamic Table
    ↓
Analytics Views
    ↓
Streamlit Dashboard
```

Automation:

```text
GitHub
   ↓
GitHub Actions
   ↓
Daily scheduled execution
   ↓
Python pipeline
   ↓
Open-Meteo
   ↓
Snowflake
```

---

# 🧠 Core Data Engineering Concepts

This project intentionally covers several important data engineering concepts.

## 1. API Data Ingestion

The pipeline consumes weather data from a REST API.

Python is responsible for:

- Sending HTTP requests.
- Passing latitude and longitude.
- Receiving JSON responses.
- Extracting nested hourly data.
- Converting API data into structured records.

---

## 2. Configuration-Driven Pipeline

Cities are not hardcoded into the ingestion logic.

They are maintained in:

```text
config/cities.json
```

Example:

```json
{
  "city": "Hyderabad",
  "latitude": 17.3850,
  "longitude": 78.4867
}
```

This allows new cities to be added without modifying the ingestion code.

---

## 3. Data Validation

Before loading data into Snowflake, the pipeline validates:

- Dataset is not empty.
- Required columns exist.
- Required fields do not contain missing values.
- All configured cities are present.
- Duplicate records are detected.

This prevents invalid data from continuing through the pipeline.

---

## 4. Cloud Data Warehousing

Snowflake acts as the central data platform.

The project uses multiple layers:

```text
RAW
 ↓
STAGING
 ↓
ANALYTICS
```

This separation makes the pipeline easier to understand, maintain, and extend.

---

## 5. Incremental Processing

Snowflake Streams are used to capture changes occurring in the RAW table.

Instead of treating the entire table as a new dataset every time, the downstream processing can work with changes captured by the stream.

---

## 6. Automated Data Processing

A Snowflake Task executes the transformation from RAW into STAGING when stream data is available.

The task uses:

```sql
SYSTEM$STREAM_HAS_DATA(...)
```

to determine whether new stream data exists.

---

## 7. Dynamic Tables

The project uses a Snowflake Dynamic Table as the analytics-ready dataset.

It contains:

- Weather measurements.
- Weather date.
- Temperature category.
- Wind category.

The Dynamic Table is configured with a target lag of one hour.

---

## 8. Analytical Views

Instead of putting all business logic inside Streamlit, reusable Snowflake views provide analytics datasets.

Examples:

- City-level weather summary.
- Daily weather summary.
- Latest weather per city.

This keeps the dashboard focused on visualization rather than data transformation.

---

## 9. Data Visualization

Streamlit provides the presentation layer.

The dashboard allows users to explore:

- City-level metrics.
- Temperature trends.
- Humidity trends.
- Precipitation.
- Latest weather conditions.
- Daily weather summaries.
- Date ranges.
- Cities dynamically.

---

## 10. Workflow Automation

GitHub Actions runs the ingestion pipeline automatically.

The current schedule is:

```text
06:00 AM IST every day
```

The GitHub Actions cron expression is:

```text
30 0 * * *
```

GitHub Actions schedules use UTC, so `00:30 UTC` corresponds to `06:00 AM IST`.

---

## 11. Secrets Management

Credentials are not stored in source code.

For local development:

```text
.env
```

is used.

For Streamlit Community Cloud:

```text
Streamlit Secrets
```

are used.

For GitHub Actions:

```text
GitHub Repository Secrets
```

are used.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion and pipeline orchestration |
| Pandas | Data processing and validation |
| Requests | API communication |
| Open-Meteo | Weather data source |
| Snowflake | Cloud data warehouse |
| Snowflake Streams | Change tracking |
| Snowflake Tasks | Incremental processing |
| Snowflake Dynamic Tables | Analytics transformation |
| Snowflake Views | Reporting datasets |
| Streamlit | Interactive dashboard |
| Git | Version control |
| GitHub | Source code repository |
| GitHub Actions | Pipeline automation |
| python-dotenv | Local environment configuration |
| PyArrow | Data transfer support for Snowflake/Pandas |

---

# 📂 Project Structure

```text
weather-data-engineering/
│
├── .github/
│   └── workflows/
│       └── weather_pipeline.yml
│
├── app/
│   ├── app.py
│   ├── queries.py
│   └── snowflake_connection.py
│
├── config/
│   └── cities.json
│
├── data/
│   └── weather_data.csv
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_raw_layer.sql
│   ├── 03_staging_layer.sql
│   ├── 04_stream.sql
│   ├── 05_task.sql
│   ├── 06_dynamic_table.sql
│   └── 07_analytics_views.sql
│
├── src/
│   ├── pipeline.py
│   │
│   ├── ingestion/
│   │   └── weather_api.py
│   │
│   ├── snowflake/
│   │   ├── connection.py
│   │   ├── load_weather.py
│   │   └── test_connection.py
│   │
│   └── validation/
│       └── validate_weather.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

> `.env` is used locally and must not be committed to GitHub.

---

# 🌐 Data Source

The project uses the **Open-Meteo API**.

API endpoint:

```text
https://api.open-meteo.com/v1/forecast
```

The pipeline requests hourly weather information for configured cities.

The main fields used are:

| API Field | Pipeline Field |
|---|---|
| `time` | `WEATHER_TIME` |
| `temperature_2m` | `TEMPERATURE` |
| `relative_humidity_2m` | `HUMIDITY` |
| `pressure_msl` | `PRESSURE` |
| `wind_speed_10m` | `WIND_SPEED` |
| `weather_code` | `WEATHER_CODE` |
| `precipitation` | `PRECIPITATION` |

---

# 🐍 Python Ingestion Pipeline

The main pipeline is:

```text
src/pipeline.py
```

It performs the following sequence:

```text
Load city configuration
        ↓
Request weather data
        ↓
Collect records from all cities
        ↓
Create Pandas DataFrame
        ↓
Validate dataset
        ↓
Load data into Snowflake
```

The pipeline also contains logging and exception handling.

A pipeline failure raises an exception, allowing automated environments such as GitHub Actions to correctly identify a failed run.

---

# ✅ Data Validation

The validation module is:

```text
src/validation/validate_weather.py
```

Validation checks include:

### Dataset validation

Ensures that the dataset contains records.

### Schema validation

Checks for required columns:

```text
city
weather_time
temperature
humidity
pressure
wind_speed
weather_code
precipitation
```

### Null validation

Checks whether required fields contain missing values.

### City validation

The validation process reads the configured cities dynamically from:

```text
config/cities.json
```

This means adding a city does not require changing the validation source code.

### Duplicate validation

The pipeline checks for duplicate records before loading.

---

# ❄️ Snowflake Architecture

The Snowflake database is:

```text
WEATHER_DB
│
├── RAW
│
├── STAGING
│
└── ANALYTICS
```

---

# 🗃️ RAW Layer

The RAW layer stores the incoming weather records.

Table:

```text
WEATHER_DB.RAW.WEATHER_RAW
```

Columns:

```text
CITY
WEATHER_TIME
TEMPERATURE
HUMIDITY
PRESSURE
WIND_SPEED
WEATHER_CODE
PRECIPITATION
```

The Python loader uses a temporary loading table and performs a `MERGE` into the RAW table using:

```text
CITY + WEATHER_TIME
```

as the matching key.

This allows existing observations to be updated and new observations to be inserted.

---

# 🔁 Snowflake Streams

The project creates:

```text
WEATHER_DB.RAW.WEATHER_RAW_STREAM
```

The Stream tracks changes made to:

```text
WEATHER_RAW
```

The downstream task can then consume the changes rather than repeatedly processing the complete RAW table.

---

# ⚙️ Snowflake Tasks

The project uses:

```text
LOAD_WEATHER_STAGING
```

The task checks whether the stream contains data:

```sql
SYSTEM$STREAM_HAS_DATA(
    'WEATHER_DB.RAW.WEATHER_RAW_STREAM'
)
```

When stream data is available, the task processes the relevant records into the STAGING layer.

---

# 🧹 STAGING Layer

The staging table is:

```text
WEATHER_DB.STAGING.WEATHER_STAGING
```

The staging transformation performs operations such as:

- Trimming city names.
- Converting city names to uppercase.
- Rounding numerical weather measurements.
- Selecting the required columns.

Example:

```sql
UPPER(TRIM(CITY))
```

and:

```sql
ROUND(TEMPERATURE, 2)
```

This creates a cleaner dataset for downstream analytics.

---

# ⚡ Dynamic Tables

The project uses:

```text
WEATHER_DB.ANALYTICS.WEATHER_ANALYTICS_DT
```

The Dynamic Table is configured with:

```text
TARGET_LAG = 1 hour
```

It derives additional analytical fields.

### Weather date

```sql
CAST(WEATHER_TIME AS DATE)
```

### Temperature category

```text
< 20°C       → COOL
20–30°C      → MODERATE
> 30°C       → HOT
```

### Wind category

```text
< 10         → LOW
10–25        → MODERATE
> 25         → HIGH
```

This demonstrates how raw measurements can be converted into business-friendly analytical attributes.

---

# 📊 Analytics Layer

The project creates three primary views.

## 1. CITY_WEATHER_SUMMARY

Provides city-level metrics:

- Total observations
- Average temperature
- Minimum temperature
- Maximum temperature
- Average humidity
- Maximum wind speed
- Total precipitation

---

## 2. DAILY_WEATHER_SUMMARY

Provides daily metrics for each city:

- Observation count
- Average temperature
- Minimum temperature
- Maximum temperature
- Average humidity
- Maximum wind speed
- Total precipitation

---

## 3. LATEST_WEATHER

Returns the latest available weather observation for every city.

It uses a window function:

```sql
ROW_NUMBER() OVER (
    PARTITION BY CITY
    ORDER BY WEATHER_TIME DESC
)
```

This makes it possible for the dashboard to display the latest observation for each city.

---

# 📈 Streamlit Dashboard

The dashboard is located at:

```text
app/app.py
```

It connects to the Snowflake ANALYTICS schema and consumes the analytical views.

## Dashboard Features

### KPI Section

Displays high-level weather metrics.

### City Comparison

Allows users to compare weather statistics between cities.

### Temperature Trends

Visualizes temperature changes over time.

### Humidity Trends

Displays humidity trends.

### Precipitation

Provides precipitation-related analysis.

### Latest Weather

Displays the latest weather data for each city.

### Daily Summary

Provides daily aggregated weather statistics.

### Dynamic City Selection

The dashboard reads available cities from Snowflake rather than maintaining a hardcoded city list.

Therefore, when a new city successfully reaches the analytics layer, it becomes available in the dashboard automatically.

---

# 🤖 Automation with GitHub Actions

The workflow is:

```text
.github/workflows/weather_pipeline.yml
```

The workflow performs:

```text
Checkout repository
        ↓
Set up Python 3.11
        ↓
Install requirements
        ↓
Run src/pipeline.py
```

The workflow supports both:

```text
Manual execution
```

and:

```text
Daily scheduled execution
```

Current schedule:

```text
00:30 UTC
06:00 AM IST
```

This allows the weather data pipeline to run without keeping VS Code or a local computer open.

---

# 🔐 Security and Secrets Management

Sensitive credentials are never intended to be stored directly in source code.

## Local Development

Local credentials are stored in:

```text
.env
```

Example structure:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=WEATHER_DB
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=your_role
```

The `.env` file is excluded through `.gitignore`.

## GitHub Actions

GitHub repository secrets are used for:

```text
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
SNOWFLAKE_DATABASE
SNOWFLAKE_SCHEMA
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_ROLE
```

## Streamlit Community Cloud

The deployed dashboard uses Streamlit Secrets for its Snowflake credentials.

This keeps credentials outside the Git repository.

---

# ☁️ Deployment

The Streamlit dashboard is deployed using:

**Streamlit Community Cloud**

Deployment configuration:

```text
Repository:
deepak4194/weather-data-engineering

Branch:
main

Main file:
app/app.py
```

The deployment connects directly to the GitHub repository.

When application changes are pushed to the repository, Streamlit Community Cloud can rebuild and redeploy the application.

---

# ➕ Adding a New City

One of the important design decisions in this project is configuration-driven ingestion.

To add a new city, update:

```text
config/cities.json
```

For example:

```json
{
  "city": "Pune",
  "latitude": 18.5204,
  "longitude": 73.8567
}
```

No change is required in:

```text
src/pipeline.py
```

or:

```text
src/validation/validate_weather.py
```

The pipeline automatically reads the configured cities.

The general flow becomes:

```text
cities.json
    ↓
Python ingestion
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
Analytics Views
    ↓
Streamlit city filter
```

---

# 💻 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/deepak4194/weather-data-engineering.git
cd weather-data-engineering
```

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Snowflake credentials

Create a local `.env` file:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=WEATHER_DB
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=your_role
```

Never commit `.env`.

---

# ▶️ Running the Pipeline

Run the complete ingestion pipeline:

```powershell
python src/pipeline.py
```

The pipeline will:

```text
Load cities
    ↓
Call Open-Meteo
    ↓
Collect weather records
    ↓
Validate data
    ↓
Load Snowflake
```

---

# 📊 Running the Dashboard Locally

Run:

```powershell
streamlit run app/app.py
```

Streamlit will start the application locally.

The deployed version uses the same application code with cloud-managed secrets.

---

# 🧪 Testing the Pipeline

The project was tested at multiple levels.

### API ingestion

Verified that weather data can be retrieved for all configured cities.

### Data validation

Verified:

- Required columns.
- Missing values.
- Configured cities.
- Duplicate records.

### Snowflake connection

Verified Python connectivity to Snowflake.

### RAW loading

Verified weather records are loaded into the RAW layer.

### Stream and Task

Verified that newly ingested records move from RAW through the Stream and Task into STAGING.

### Dynamic Table

Verified that the Dynamic Table refreshes and includes newly added cities.

### Streamlit

Verified that the dashboard loads Snowflake analytics and dynamically reflects newly available cities.

### GitHub Actions

Verified that the automated workflow can execute the pipeline successfully.

### Deployment

Verified the Streamlit Community Cloud deployment and Snowflake connection.

---

# 🧩 Key Engineering Decisions

## Configuration instead of hardcoding

Cities are maintained in JSON so the ingestion process can scale to additional locations without changing pipeline logic.

## Layered Snowflake architecture

Separating:

```text
RAW → STAGING → ANALYTICS
```

makes the data flow easier to understand and maintain.

## Bulk loading

The Python loader uses Snowflake's Pandas integration to efficiently transfer batches of records.

## MERGE-based RAW loading

The loader matches records using:

```text
CITY + WEATHER_TIME
```

and inserts new records while updating matching records.

## Incremental downstream processing

Streams and Tasks are used to demonstrate change-driven processing rather than repeatedly rebuilding the entire staging dataset.

## Analytics separated from visualization

Business transformations are performed in Snowflake rather than inside Streamlit.

This keeps the dashboard primarily focused on querying and visualization.

## Cloud automation

GitHub Actions removes the dependency on a local machine for daily ingestion.

---

# 📚 What This Project Demonstrates

This project provides practical exposure to the following data engineering concepts:

### Python

- REST API integration
- JSON processing
- Pandas
- Data validation
- Logging
- Exception handling
- Environment variables
- Modular project structure

### Snowflake

- Databases and schemas
- Tables
- Temporary tables
- Stages and file formats
- Bulk loading
- MERGE
- Streams
- Tasks
- Dynamic Tables
- Views
- SQL transformations
- Window functions
- Aggregations

### Data Engineering

- ETL/ELT concepts
- Layered architecture
- Incremental processing
- Configuration-driven pipelines
- Data quality
- Cloud data warehousing
- Analytics modeling
- Pipeline automation

### DevOps

- Git
- GitHub
- GitHub Actions
- Scheduled workflows
- Repository secrets
- CI/CD-style automation

### Data Applications

- Streamlit
- Interactive filtering
- Data visualization
- Cloud deployment
- Secrets management

---

# 🔮 Future Improvements

The current project provides a complete working pipeline, but it can be extended further.

Possible improvements include:

- Add more geographical locations.
- Add historical weather tracking.
- Add weather alerts.
- Add additional weather variables.
- Add automated data-quality reporting.
- Add pipeline monitoring and alerting.
- Add automated tests to the GitHub Actions workflow.
- Add unit tests for ingestion and validation modules.
- Add more advanced Snowflake transformations.
- Improve incremental handling for updated records across downstream layers.
- Add a dedicated orchestration platform for larger-scale workflows.
- Add dashboard authentication if required.
- Add data freshness monitoring.

---

# 🎓 Learning Outcomes

By building this project, the following concepts were applied together rather than studied independently:

```text
API Integration
      +
Python Programming
      +
Data Validation
      +
Snowflake
      +
Streams
      +
Tasks
      +
Dynamic Tables
      +
SQL Analytics
      +
Git/GitHub
      +
GitHub Actions
      +
Streamlit
      +
Cloud Deployment
```

The project therefore demonstrates the complete journey of data from an external source to a user-facing analytical application.

---

# 🏁 Conclusion

The **Weather Data Engineering Pipeline** is an end-to-end cloud data engineering project designed to demonstrate how raw API data can be transformed into a reliable analytical application.

The final system combines:

```text
External API
     ↓
Python
     ↓
Data Validation
     ↓
Snowflake RAW
     ↓
Streams
     ↓
Tasks
     ↓
STAGING
     ↓
Dynamic Table
     ↓
Analytics Views
     ↓
Streamlit
```

with automated execution through:

```text
GitHub Actions
      ↓
Daily Pipeline
```

and cloud deployment through:

```text
Streamlit Community Cloud
```

The project demonstrates practical knowledge across **data ingestion, cloud warehousing, incremental processing, transformation, analytics, automation, security, visualization, and deployment**.

---

## 👨‍💻 Author

**Deepak Mandarapu**

B.Tech — Computer Science & Engineering (Artificial Intelligence & Machine Learning)

GitHub:  
https://github.com/deepak4194

---

## ⭐ Project

If you find this project useful or are learning data engineering, feel free to explore the repository and the implementation.

**Built with Python, Snowflake, Open-Meteo, GitHub Actions, and Streamlit.**
