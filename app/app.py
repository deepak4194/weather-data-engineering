import pandas as pd
import streamlit as st

from snowflake_connection import get_snowflake_connection
from queries import (
    CITY_SUMMARY_QUERY,
    DAILY_SUMMARY_QUERY,
    LATEST_WEATHER_QUERY,
    WEATHER_TREND_QUERY,
)


st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide",
)


# ---------------------------------------------------------
# Snowflake connection
# ---------------------------------------------------------

@st.cache_resource
def get_connection():
    return get_snowflake_connection()


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

@st.cache_data(ttl=300)
def load_data():

    connection = get_connection()

    city_summary = connection.query(
        CITY_SUMMARY_QUERY,
        ttl=300,
    )

    daily_summary = connection.query(
        DAILY_SUMMARY_QUERY,
        ttl=300,
    )

    latest_weather = connection.query(
        LATEST_WEATHER_QUERY,
        ttl=300,
    )

    weather_trend = connection.query(
        WEATHER_TREND_QUERY,
        ttl=300,
    )

    return (
        city_summary,
        daily_summary,
        latest_weather,
        weather_trend,
    )


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

st.title("🌦️ Weather Analytics Dashboard")

st.markdown(
    """
    ### Weather Data Engineering Pipeline

    Real-time weather data collected from **Open-Meteo**,
    processed using **Python and Snowflake**, and presented
    through this interactive analytics dashboard.
    """
)


try:

    (
        city_summary,
        daily_summary,
        latest_weather,
        weather_trend,
    ) = load_data()

except Exception as error:

    st.error(
        "Unable to connect to Snowflake or load analytics data."
    )

    st.exception(error)

    st.stop()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------

st.sidebar.header("🔎 Filters")

cities = sorted(city_summary["CITY"].unique())

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + cities,
)


# Convert date column
daily_summary["WEATHER_DATE"] = pd.to_datetime(
    daily_summary["WEATHER_DATE"]
)


min_date = daily_summary["WEATHER_DATE"].min().date()
max_date = daily_summary["WEATHER_DATE"].max().date()


selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------

filtered_daily = daily_summary.copy()

if selected_city != "All Cities":

    filtered_daily = filtered_daily[
        filtered_daily["CITY"] == selected_city
    ]


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_daily = filtered_daily[
        (
            filtered_daily["WEATHER_DATE"].dt.date >= start_date
        )
        &
        (
            filtered_daily["WEATHER_DATE"].dt.date <= end_date
        )
    ]


# ---------------------------------------------------------
# KPI section
# ---------------------------------------------------------

st.subheader("📊 Key Metrics")


if selected_city == "All Cities":

    avg_temperature = city_summary["AVG_TEMPERATURE"].mean()

    avg_humidity = city_summary["AVG_HUMIDITY"].mean()

    max_wind = city_summary["MAX_WIND_SPEED"].max()

    total_precipitation = city_summary[
        "TOTAL_PRECIPITATION"
    ].sum()

else:

    selected_summary = city_summary[
        city_summary["CITY"] == selected_city
    ].iloc[0]

    avg_temperature = selected_summary["AVG_TEMPERATURE"]

    avg_humidity = selected_summary["AVG_HUMIDITY"]

    max_wind = selected_summary["MAX_WIND_SPEED"]

    total_precipitation = selected_summary[
        "TOTAL_PRECIPITATION"
    ]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌡️ Average Temperature",
        f"{avg_temperature:.2f} °C",
    )


with col2:

    st.metric(
        "💧 Average Humidity",
        f"{avg_humidity:.2f} %",
    )


with col3:

    st.metric(
        "💨 Maximum Wind",
        f"{max_wind:.2f} km/h",
    )


with col4:

    st.metric(
        "🌧️ Total Precipitation",
        f"{total_precipitation:.2f} mm",
    )


st.divider()


# ---------------------------------------------------------
# City comparison
# ---------------------------------------------------------

st.subheader("🏙️ City Weather Comparison")


tab1, tab2, tab3 = st.tabs(
    [
        "🌡️ Temperature",
        "💧 Humidity",
        "💨 Wind",
    ]
)


with tab1:

    st.bar_chart(
        city_summary.set_index("CITY")[
            "AVG_TEMPERATURE"
        ]
    )


with tab2:

    st.bar_chart(
        city_summary.set_index("CITY")[
            "AVG_HUMIDITY"
        ]
    )


with tab3:

    st.bar_chart(
        city_summary.set_index("CITY")[
            "MAX_WIND_SPEED"
        ]
    )


st.divider()


# ---------------------------------------------------------
# Weather trends
# ---------------------------------------------------------

st.subheader("📈 Weather Trends")


trend_data = weather_trend.copy()

trend_data["WEATHER_TIME"] = pd.to_datetime(
    trend_data["WEATHER_TIME"]
)


if selected_city != "All Cities":

    trend_data = trend_data[
        trend_data["CITY"] == selected_city
    ]


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

    trend_data = trend_data[
        (
            trend_data["WEATHER_TIME"].dt.date >= start_date
        )
        &
        (
            trend_data["WEATHER_TIME"].dt.date <= end_date
        )
    ]


trend_data = trend_data.sort_values(
    "WEATHER_TIME"
)


if not trend_data.empty:

    st.markdown("#### Temperature Over Time")

    temperature_chart = trend_data.pivot(
        index="WEATHER_TIME",
        columns="CITY",
        values="TEMPERATURE",
    )

    st.line_chart(temperature_chart)


    st.markdown("#### Humidity Over Time")

    humidity_chart = trend_data.pivot(
        index="WEATHER_TIME",
        columns="CITY",
        values="HUMIDITY",
    )

    st.line_chart(humidity_chart)


    st.markdown("#### Precipitation Over Time")

    precipitation_chart = trend_data.pivot(
        index="WEATHER_TIME",
        columns="CITY",
        values="PRECIPITATION",
    )

    st.bar_chart(precipitation_chart)

else:

    st.info("No weather data available for the selected filters.")


st.divider()


# ---------------------------------------------------------
# Latest weather
# ---------------------------------------------------------

st.subheader("🌤️ Latest Weather")


latest_display = latest_weather.copy()

latest_display["WEATHER_TIME"] = pd.to_datetime(
    latest_display["WEATHER_TIME"]
)


if selected_city != "All Cities":

    latest_display = latest_display[
        latest_display["CITY"] == selected_city
    ]


latest_display = latest_display.rename(
    columns={
        "CITY": "City",
        "WEATHER_TIME": "Time",
        "TEMPERATURE": "Temperature (°C)",
        "HUMIDITY": "Humidity (%)",
        "PRESSURE": "Pressure (hPa)",
        "WIND_SPEED": "Wind Speed (km/h)",
        "PRECIPITATION": "Precipitation (mm)",
        "WEATHER_CODE": "Weather Code",
        "TEMP_CATEGORY": "Temperature Category",
        "WIND_CATEGORY": "Wind Category",
    }
)


st.dataframe(
    latest_display,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# Daily summary
# ---------------------------------------------------------

st.divider()

st.subheader("📅 Daily Weather Summary")


daily_display = filtered_daily.rename(
    columns={
        "CITY": "City",
        "WEATHER_DATE": "Date",
        "OBSERVATIONS": "Observations",
        "AVG_TEMPERATURE": "Avg Temperature (°C)",
        "MIN_TEMPERATURE": "Min Temperature (°C)",
        "MAX_TEMPERATURE": "Max Temperature (°C)",
        "AVG_HUMIDITY": "Avg Humidity (%)",
        "MAX_WIND_SPEED": "Max Wind Speed (km/h)",
        "TOTAL_PRECIPITATION": "Total Precipitation (mm)",
    }
)


st.dataframe(
    daily_display,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Data source: Open-Meteo | "
    "Data platform: Snowflake | "
    "Application: Streamlit"
)