import pandas as pd


FILE_PATH = "data/weather_data.csv"

EXPECTED_CITIES = {
    "Hyderabad",
    "Vijayawada",
    "Chennai",
    "Bengaluru",
    "Mumbai",
    "Delhi"
}


def validate_weather_data(df):
    errors = []

    # Check 1: records exist
    if df.empty:
        errors.append("Dataset contains no records.")

    # Check 2: required columns exist
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

    # Stop further checks if required columns are missing
    if errors:
        return errors

    # Check 3: missing values
    missing_values = df[list(required_columns)].isnull().sum()

    columns_with_missing_values = (
        missing_values[missing_values > 0]
    )

    if not columns_with_missing_values.empty:
        errors.append(
            "Missing values found: "
            + str(columns_with_missing_values.to_dict())
        )

    # Check 4: expected cities
    actual_cities = set(df["city"].unique())

    missing_cities = EXPECTED_CITIES - actual_cities

    if missing_cities:
        errors.append(
            f"Missing expected cities: {sorted(missing_cities)}"
        )

    # Check 5: duplicate records
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