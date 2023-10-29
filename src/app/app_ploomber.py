import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import pickle  # Import the pickle module to load the ARIMA model
import datetime
import duckdb
import os
from pathlib import Path

# Get MotherDuck token
#md_token = os.getenv('MOTHERDUCK_TOKEN')

# Connect to MotherDuck database
#motherduck_con = duckdb.connect(f'md:?motherduck_token={md_token}')

# Query database and output into pandas dataframe
#air_data_df = motherduck_con.sql("SELECT * FROM openaq_api.main.df").df()

#current_dir = os.getcwd()
#print(current_dir)
#parent_directory = os.path.dirname(current_dir)
#print(parent_directory)
#database_directory = os.path.join(parent_directory, "data", "air_data.duckdb")
#print(database_directory)
#con = duckdb.connect(database_directory)
#result = con.execute("SELECT * FROM air_data;")
#df = result.fetch_df()



from dotenv import load_dotenv

# Load MotherDuck token
load_dotenv('.env')

# Get MotherDuck token
md_token = os.getenv('MOTHERDUCK_TOKEN')

# Connect to MotherDuck database
motherduck_con = duckdb.connect(f'md:?motherduck_token={md_token}')

# Query database and output into pandas dataframe
air_data_df = motherduck_con.sql("SELECT * FROM openaq_api.main.df").df()




df = air_data_df
df.head()

#con.close()

# Create a Streamlit app title
st.title("AirQ-Forecaster")

# Define two tabs
tabs = ["Data Visualizations", "Make Predictions"]
selected_tab = st.radio("Select Tab:", tabs)

# Load dataset
#df = pd.read_csv('EDA_ploomber.csv')

# If "Make Predictions" tab is selected
if selected_tab == "Make Predictions":
    st.header("Make AQI Predictions")
    
    #model_path = os.path.join(parent_directory, "notebooks", "ML", "arima_model.pkl")
    
    # Load the saved ARIMA model
    model_file = 'arima_model.pkl'
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    
    # Add user input for forecast date
    forecast_date = st.date_input("Select Forecast Date", datetime.date(2023, 10, 21))
        
    # Convert 'date.local' to object if needed
    df['date.local'] = df['date.local'].astype(str)
        
    # Split the string by space to separate the date and time
    date_time_parts = df['date.local'][0].split(' ')
    
    # Split the date part by '-' to get the year, month, and day
    date_parts = date_time_parts[0].split('-')

    # Convert the date parts to integers
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    current_date = datetime.date(year, month, day)
    #current_date = datetime.date(2023, 10, 20)
    
    # Calculate the number of forecast periods from the current date to the forecast date
    forecast_periods = (forecast_date - current_date).days
    
    if forecast_periods <= 0:
        st.write('The specified date is in the measured data (no prediction necessary)')
    else:
        # Use your ARIMA model to make a forecast for the given date
        forecasted_values = model.forecast(steps=forecast_periods)
    
        # Take the last forecasted value, which corresponds to the specified date
        forecasted_value = forecasted_values[-1]
    
        # AQI bucketing
        def get_AQI_bucket(x):
            if x <= 50:
                return "Good"
            elif x <= 100:
                return "Satisfactory"
            elif x <= 200:
                return "Moderate"
            elif x <= 300:
                return "Poor"
            elif x <= 400:
                return "Very Poor"
            elif x > 400:
                return "Severe"
            else:
                return "Not defined"
    
        AQI_classification = get_AQI_bucket(forecasted_value)
    
        # Display the prediction
        if st.button("Get AQI Prediction"):
            st.write(f"Predicted AQI for {forecast_date}: {forecasted_value}, {AQI_classification}")

# If "Data Visualizations" tab is selected
if selected_tab == "Data Visualizations":
    st.header("Data Visualizations")
    
    # Convert 'date.local' to datetime if needed
    df['date.local'] = pd.to_datetime(df['date.local'])
    
    # Create a list of unique parameter options
    parameter_options = df['parameter'].unique()

    # Add a selectbox for choosing the parameter
    selected_parameter = st.selectbox("Select Parameter", parameter_options)
    
    # Statistics
    df_stat = df['value'][df["parameter"] == selected_parameter].describe()
    st.subheader(f'Statistics for {selected_parameter}')
    df_stat
    
    # Filter the dataFrame for the selected parameter
    subset = df[df['parameter'] == selected_parameter]
    
    # Create a time series plot
    st.subheader("Complete time serie")
    fig = plt.figure()
    plt.plot(subset['date.local'], subset['value'])
    plt.xlabel("Time")
    plt.ylabel(selected_parameter)
    st.pyplot(fig)
    
    # Daily mean
    df_mean = df.groupby(['parameter', df['date.local'].dt.date])['value'].mean().reset_index()
    
    # Pivot table with columns for each variable
    pivoted_df = df.pivot_table(index=df['date.local'], columns='parameter', values='value')
    
    # Filter the dataFrame for the selected parameter
    subset = df_mean[df_mean['parameter'] == selected_parameter]

    # Create the plot
    st.subheader("Time serie - Daily mean")
    fig = plt.figure()
    plt.plot(subset['date.local'], subset['value'], label=selected_parameter)
    plt.xlabel('Time')
    plt.ylabel(selected_parameter)
    st.pyplot(fig)
    
    # Function to calculate the Sub_Index for the Air Quality Index (AIQ)

    ## PM2.5 Sub-Index calculation
    def get_PM25_subindex(x):
        if x <= 30:
            return x * 50 / 30
        elif x <= 60:
            return 50 + (x - 30) * 50 / 30
        elif x <= 90:
            return 100 + (x - 60) * 100 / 30
        elif x <= 120:
            return 200 + (x - 90) * 100 / 30
        elif x <= 250:
            return 300 + (x - 120) * 100 / 130
        elif x > 250:
            return 400 + (x - 250) * 100 / 130
        else:
            return 0

    ## PM10 Sub-Index calculation
    def get_PM10_subindex(x):
        if x <= 50:
            return x
        elif x <= 100:
            return x
        elif x <= 250:
            return 100 + (x - 100) * 100 / 150
        elif x <= 350:
            return 200 + (x - 250)
        elif x <= 430:
            return 300 + (x - 350) * 100 / 80
        elif x > 430:
            return 400 + (x - 430) * 100 / 80
        else:
            return 0    
        
    # Function for defining the AQI value and its category (Good, Satisfactory, Moderate, Poor, Very Poor and Severe)

    ## AQI bucketing
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x <= 100:
            return "Satisfactory"
        elif x <= 200:
            return "Moderate"
        elif x <= 300:
            return "Poor"
        elif x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return np.NaN
        
    # Pivot table with daily means per variable
    df_mean_day = df_mean.pivot_table(index=df_mean['date.local'], columns='parameter', values='value').reset_index()

    # Subindex    
    df_mean_day["pm25_SubIndex"] = df_mean_day["pm25"].apply(lambda x: get_PM25_subindex(x))
    df_mean_day["pm10_SubIndex"] = df_mean_day["pm10"].apply(lambda x: get_PM10_subindex(x))

    # AQI value
    df_mean_day["AQI_calculated"] = round(df_mean_day[["pm25_SubIndex", "pm10_SubIndex"]].max(axis = 1))
    df_mean_day.loc[df_mean_day["pm25_SubIndex"] + df_mean_day["pm10_SubIndex"] <= 0, "AQI_calculated"] = np.NaN
    df_mean_day.loc["AQI_calculated"] = np.NaN

    # AQI classification
    df_mean_day["AQI_bucket_calculated"] = df_mean_day["AQI_calculated"].apply(lambda x: get_AQI_bucket(x))
    #df_mean_day[~df_mean_day.AQI_calculated.isna()]
    
    # Convert 'date.local' to datetime if needed
    df_mean_day['date.local'] = pd.to_datetime(df_mean_day['date.local'])

    # Time series for AQI
    st.subheader("Time serie for AQI")
    fig = plt.figure()
    plt.plot(df_mean_day['date.local'], df_mean_day['AQI_calculated'])
    plt.xlabel('Time')
    plt.ylabel('AQI value')
    
    # Define AQI classification thresholds and labels
    aqi_thresholds = [50, 100, 200, 300, 400, float('inf')]
    aqi_labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

    # Draw horizontal lines for AQI classification thresholds
    for i in range(len(aqi_thresholds) - 1):
        threshold = aqi_thresholds[i]
        label = aqi_labels[i]
        plt.axhline(y=threshold, color='r', linestyle='--')
        # Add labels to the lines
        plt.text(plt.xlim()[1], threshold, f'{label}', va='center', ha='right')

    st.pyplot(fig)
    