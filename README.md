
![Ploomber Logo](https://github.com/beltran-oscar/ETL-pipeline-ML/blob/main/images/ploomber-logo.png)


# AirQ-Forecaster: An ETL-to-ML Pipeline for Predicting Air Quality Index
### Hacktoberfest 2023 - Ploomber Mentorship Program
 

## Description

This project focuses on creating an ETL (Extract, Transform, Load) pipeline with Ploomberfor air quality data. The pipeline fetches and processes air quality measurements from the OpenAQ API and uses DuckDB and MotherDuck for data storage and management.

We implemented the **ARIMA** (AutoRegressive Integrated Moving Average) model for time series forecasting to predict the Air Quality Index. ARIMA is a powerful and widely-used statistical method effective for short-term forecasting with data having seasonality, or cyclic patterns.

Key Features of ARIMA:

- **AutoRegressive (AR):** Leverages the relationship between an observation and a number of lagged observations (autoregression).

- **Integrated (I):** Involves differencing the time series to make it stationary, i.e., to stabilize the mean of the time series by removing changes in the level.

- **Moving Average (MA):** Models the error term as a linear combination of error terms at various times in the past.

## Data sources

**OpenAQ** - API designed for aggregating and sharing open air quality data from around the world.

We used an air quality sensor with location ID 380422 (49.208733, -122.9118), located in the city of New Westminster in British Columbia, Canada.

### Parameters

- `pm1 - PM1` ➡️ Particulate matter less than 1 micrometer in diameter mass concentration, µg/m³
- `pm10 - PM10` ➡️ Particulate matter less than 10 micrometers in diameter mass concentration, µg/m³
- `pm25 - PM2.5` ➡️ Particulate matter less than 2.5 micrometers in diameter mass concentration, µg/m³
- `um003 - PM0.3` ➡️ count, particles/cm³
- `um005 - PM0.5` ➡️ count, particles/cm³
- `um010 - PM1` ➡️ count, particles/cm³
- `um025 - PM2.5` ➡️ count, particles/cm³
- `um050 - PM5.0` ➡️ count, particles/cm³
- `um100 - PM10` ➡️ count, particles/cm³
- `pressure` ➡️ Atmospheric or barometric pressure, hPa
- `temperature` ➡️ °C
- `humidity` ➡️ %

## Methods

![Flowchart](https://github.com/beltran-oscar/ETL-pipeline-ML/blob/main/images/flowchart.png)

- **GitHub Actions**: The ETL process is automatically executed every hour.

- **Ploomber Pipeline:** The ETL process is managed using Ploomber, a workflow management tool. The pipeline configuration can be found in `pipeline.yaml`.

- **Data Extraction and Cloud Data Storage MotherDuck:** The data extraction process fetches air quality measurements from the OpenAQ API. The extraction logic is implemented in `extract_duckdb.py`. The extracted data is stored in the cloud using MotherDuck.

- **Jupyter Notebooks:** The project includes Jupyter notebooks for data exploration and analysis (see `extract.ipynb`).

- **Docker Integration:** The project is containerized using Docker, allowing for easy setup and deployment. The Dockerfile provides the necessary instructions to build the Docker image.

## Dependencies

See `pyproject.toml` for all package requirements. Dependencies are managed using `poetry`.

## User Interface 

The Streamlit App is deployed in [Ploomber Cloud](https://ploomber.io/cloud/). You can access the app [here](https://weathered-heart-8302.ploomberapp.io/) or by following this URL: https://weathered-heart-8302.ploomberapp.io/


![Streamlit App](https://github.com/beltran-oscar/ETL-pipeline-ML/blob/main/images/app-streamlit.gif)

## Authors

Alejandro Leiva - [aleivaar94](https://github.com/aleivaar94)

Oscar Beltrán - [beltran-oscar](https://github.com/beltran-oscar)

## Acknowledgments

We want to thank the [Ploomber](https://ploomber.io/) Team for their time and dedicated mentorship during the development of this project. Special mention to [Laura Funderburk](https://github.com/lfunderburk) - Developer Advocate at Ploomber, for her patience and dedication to guide all mentees.

We also want to thank [Eduardo Blancas](https://github.com/edublancas) - Co-founder/CEO at Ploomber for this mentorship opportunity.

## License
The project is licensed under the Apache 2.0 License.