from datetime import datetime
from io import StringIO
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.timeanddate.com/weather/"

chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=chrome_options)


try:
    print("Opening weather website...")

    driver.get(URL)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "table")
        )
    )

    time.sleep(3)

    print(f"Page title: {driver.title}")

    # Copy the loaded HTML so Selenium is no longer
    # needed while processing individual records.
    page_html = driver.page_source

finally:
    driver.quit()


# Read all HTML tables from the page.
tables = pd.read_html(StringIO(page_html))

weather_tables = []

for table in tables:
    table.columns = [
        str(column).strip()
        for column in table.columns
    ]

    lowercase_columns = [
        column.lower()
        for column in table.columns
    ]

    if (
        any("city" in column for column in lowercase_columns)
        and any("country" in column for column in lowercase_columns)
        and any("temp" in column for column in lowercase_columns)
    ):
        weather_tables.append(table)


if not weather_tables:
    raise ValueError(
        "The weather table could not be found."
    )


# Use the largest matching table.
weather_table = max(
    weather_tables,
    key=len
)

print(f"Weather rows found: {len(weather_table)}")


def find_column(dataframe, search_text):
    for column in dataframe.columns:
        if search_text in column.lower():
            return column

    raise ValueError(
        f"Column containing '{search_text}' was not found."
    )


city_column = find_column(weather_table, "city")
country_column = find_column(weather_table, "country")
condition_column = find_column(weather_table, "condition")
temperature_column = find_column(weather_table, "temp")
wind_column = find_column(weather_table, "wind")
time_column = find_column(weather_table, "time")


# Create a DataFrame with consistent column names.
raw_df = pd.DataFrame({
    "City": weather_table[city_column],
    "Country": weather_table[country_column],
    "Condition": weather_table[condition_column],
    "Temperature": weather_table[temperature_column],
    "Wind": weather_table[wind_column],
    "Local Time": weather_table[time_column]
})


print("\nRaw data:")
print(raw_df.head())

print(f"\nRaw row count: {len(raw_df)}")


# Save the unmodified scraped data.
raw_df.to_csv(
    "weather_raw.csv",
    index=False
)

print("Created weather_raw.csv")


# Create a cleaned copy.
clean_df = raw_df.copy()

clean_df.columns = [
    "city",
    "country",
    "condition",
    "temperature_f",
    "wind_mph",
    "local_time"
]


# Convert blank or unavailable values to missing values.
clean_df = clean_df.replace(
    [
        "",
        "?Not available",
        "Not available",
        "nan"
    ],
    pd.NA
)


# Extract numeric temperature values.
clean_df["temperature_f"] = pd.to_numeric(
    clean_df["temperature_f"]
    .astype("string")
    .str.extract(r"(-?\d+)", expand=False),
    errors="coerce"
)


# Extract numeric wind-speed values.
clean_df["wind_mph"] = pd.to_numeric(
    clean_df["wind_mph"]
    .astype("string")
    .str.extract(r"(\d+)", expand=False),
    errors="coerce"
)


# Remove duplicate city records.
clean_df = clean_df.drop_duplicates(
    subset=["city", "country"]
)


# Remove records missing essential values.
clean_df = clean_df.dropna(
    subset=[
        "city",
        "country",
        "temperature_f"
    ]
)


# Record when the data was collected.
clean_df["scraped_at"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

clean_df = clean_df.reset_index(drop=True)


print("\nClean data:")
print(clean_df.head())

print(f"\nClean row count: {len(clean_df)}")

print("\nMissing values after cleaning:")
print(clean_df.isna().sum())


# Save the cleaned data.
clean_df.to_csv(
    "weather_clean.csv",
    index=False
)

print("\nCreated weather_clean.csv")