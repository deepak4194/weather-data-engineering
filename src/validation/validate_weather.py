import pandas as pd


FILE_PATH = "data/weather_data.csv"


df = pd.read_csv(FILE_PATH)


print("===== DATASET OVERVIEW =====")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== CITIES =====")
print(df["city"].unique())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE RECORDS =====")
print(df.duplicated().sum())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== TIME RANGE =====")
print("Start:", df["weather_time"].min())
print("End:", df["weather_time"].max())

print("\n===== NUMERIC SUMMARY =====")
print(
    df[
        [
            "temperature",
            "humidity",
            "pressure",
            "wind_speed",
            "precipitation"
        ]
    ].describe()
)