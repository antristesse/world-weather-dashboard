# world-weather-dashboard

This project collects current weather data from the Time and Date Weather Around the World website. Selenium loads the live webpage, and pandas extracts, cleans, and saves the weather data for future analysis and visualization.

## Current Progress

The web scraper collects:

- City
- Country
- Weather condition
- Temperature
- Wind speed
- Local time
- Scraping timestamp

The program saves both the original scraped data and a cleaned version.

## Files

- `scrape_weather.py` — scrapes and cleans the weather data
- `weather_raw.csv` — original scraped data
- `weather_clean.csv` — cleaned weather data
- `requirements.txt` — required Python packages

## Setup

Install the required packages:

```bash
python -m pip install -r requirements.txt

```

## Run the Scraper

```bash
python scrape_weather.py
```

The script opens Chrome, retrieves the current weather table, and creates the raw and cleaned CSV files.

## Data Source

[Time and Date: Weather Around the World](https://www.timeanddate.com/weather/)

## Future Development

The project will later store the cleaned data in SQLite and display interactive weather visualizations in a Streamlit dashboard.