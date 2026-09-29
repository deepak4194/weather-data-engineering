import json
import pandas as pd


FILE_PATH = "data/weather_data.csv"
CITIES_FILE_PATH = "config/cities.json"


def load_expected_cities():
    with open(CITIES_FILE_PATH, "r", encoding="utf-8") as file:
        cities = json.load(file)

    return {
        city["city"].upper()
        for city in cities
    }


def validate_weather_data(df):
    errors = []

    if df.empty:
        errors.append("Dataset contains no records.")

    required_columns = {
        "city",
        "weather_time",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "weather_code",
        "precipitation"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        errors.append(
            f"Missing columns: {sorted(missing_columns)}"
        )

    if errors:
        return errors

    missing_values = df[list(required_columns)].isnull().sum()

    columns_with_missing_values = (
        missing_values[missing_values > 0]
    )

    if not columns_with_missing_values.empty:
        errors.append(
            "Missing values found: "
            + str(columns_with_missing_values.to_dict())
        )

    expected_cities = load_expected_cities()

    actual_cities = {
        city.upper()
        for city in df["city"].dropna().unique()
    }

    missing_cities = expected_cities - actual_cities

    if missing_cities:
        errors.append(
            f"Missing expected cities: {sorted(missing_cities)}"
        )

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        errors.append(
            f"Found {duplicate_count} duplicate records."
        )

    return errors


def main():
    df = pd.read_csv(FILE_PATH)

    print("===== DATASET VALIDATION =====")

    errors = validate_weather_data(df)

    if errors:
        print("\n❌ VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        raise ValueError("Weather data validation failed.")

    print("\n✅ VALIDATION PASSED")
    print(f"Records: {len(df)}")
    print(f"Cities: {len(df['city'].unique())}")


if __name__ == "__main__":
    main()