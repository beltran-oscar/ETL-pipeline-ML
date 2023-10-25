

# AirQ-Forecaster: An ETL-to-ML Pipeline for Predicting Air Quality Index
### Hacktoberfest 2023 - Ploomber Mentorship Program
 

## Description

This project focuses on creating an ETL (Extract, Transform, Load) pipeline with Ploomberfor air quality data. The pipeline fetches and processes air quality measurements from the OpenAQ API and uses DuckDB and MotherDuckDB for data storage and management.

We implemented the **ARIMA** (AutoRegressive Integrated Moving Average) model for time series forecasting to predict the Air Quality Index. ARIMA is a powerful and widely-used statistical method effective for short-term forecasting with data having seasonality, or cyclic patterns.

Key Features of ARIMA:

- **AutoRegressive (AR):** Leverages the relationship between an observation and a number of lagged observations (autoregression).

- **Integrated (I):** Involves differencing the time series to make it stationary, i.e., to stabilize the mean of the time series by removing changes in the level.

- **Moving Average (MA):** Models the error term as a linear combination of error terms at various times in the past.

## Data sources

OpenAQ: API designed for aggregating and sharing open air quality data from around the world.

We used an air quality sensor with location ID 380422 (49.208733, -122.9118), located in the city of New Westminster in British Columbia, Canada.

## Methods / Métodos

**Include Process Flow Diagram Here (Pending)**

## User interface 

**Flask app Dashboard (PENDING)**

## Authors

Alejandro Leiva - [aleivaar94](https://github.com/aleivaar94)

Oscar Beltrán - [beltran-oscar](https://github.com/beltran-oscar)

## Acknowledgments

We want to thank the [Ploomber](https://ploomber.io/) Team for their time and dedicated mentorship during the development of this project. Special mention to [Laura Funderburk](https://github.com/lfunderburk) - Developer Advocate at Ploomber, for her commitment and dedication to guide all mentees.

We also like to specially thank [Eduardo Blancas](https://github.com/edublancas) - Co-founder/CEO at Ploomber for this mentorship opportunity.
