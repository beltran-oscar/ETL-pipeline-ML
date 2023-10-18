# %% tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None

# %%
import requests
import pandas as pd
import os
import duckdb
import seaborn as sns
import matplotlib.pyplot as plt
import pytz
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Setting pandas to display all columns and rows 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# %%
def extract(api_key):
    """
    Fetch and process air quality measurements from the OpenAQ API.

    Parameters
    ----------
    api_key : str
        API key for authentication with the OpenAQ API.

    Returns
    -------
    df : pandas.DataFrame
        Dataframe containing the fetched measurements.
        
    Raises
    ------
    requests.exceptions.HTTPError
        For HTTP related errors.
    requests.exceptions.ConnectionError
        For connection related errors.
    requests.exceptions.Timeout
        For timeout errors.
    requests.exceptions.RequestException
        For all other request related errors.
    Exception
        If the fetched dataframe is empty.

    """
    
    # API URL
    api_url = "https://api.openaq.org/v2/measurements"
    
    # Define the query parameters to API
    params = {
        "location_id": "380422",
        "parameter": ["pressure", "temperature", "um003", "um025", "um010", "pm10", "um100", "pm1", "um005", "humidity", "um050", "pm25"],
        "limit": 10000,
        "api_key": api_key
    }
    
    try:
        # Make the GET request
        response = requests.get(api_url, params=params)
        
        # Raise exception for HTTP errors
        response.raise_for_status()
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            output = pd.json_normalize(data['results'])
            df = pd.DataFrame(output)
            
            # Check if dataframe is empty
            if df.empty:
                raise Exception("Empty df, check API request")
            
            df['date.utc'] = pd.to_datetime(df['date.utc'], errors='coerce') # Convert to datetime
            df['date.local'] = df['date.utc'].dt.tz_convert('America/Los_Angeles') # Covert to PST/PDT time zone
            df['date.local'] = df['date.local'].dt.tz_localize(None) # Convert to timezone-naive
            df = df[df['value'] > 0.0] # Filter values
            
            return df
        
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error: Something Else", err)
    except Exception as e:
        print(e)

# %%
# Create local DuckDB instance
def init_duckdb(df, table_name, database_directory):
    """
    Initiate a DuckDB instance to create a DuckDB database named "air_data.duckdb" inside the
    given `database_directory` if it does not already exist. If the specified `table_name`
    does not exist in the database, it will be created and the given DataFrame `df`
    will be stored in it.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be registered and stored in the DuckDB database.
    table_name : str
        Name of the table in which the DataFrame should be stored.
    database_directory : str
        Directory path where the DuckDB database file ("air_data.duckdb") will be located.

    Returns
    -------
    None

    """
    duckdb_directory = os.path.join(database_directory, "air_data.duckdb")
    con = duckdb.connect(duckdb_directory)
    con.register('df', df)
    
    # Check if table already exists, if not, create it
    tables = con.execute("SHOW TABLES").fetchall()
    if table_name not in [table[0] for table in tables]:
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    
    con.close()

# %%
if __name__ == "__main__":
    # Load API key from .env file
    load_dotenv('.env')
    api_key = os.getenv('API_KEY')
    
    # Call extract function
    df = extract(api_key)
    df.info()

    # Define table name
    table_name = "air_data"

    # Define current working directory
    current_dir = os.getcwd()

    # Get parent directory
    parent_directory = os.path.dirname(current_dir)

    # Define directory to store DuckDB database
    database_directory = os.path.join(parent_directory, "data")

    # Call save_to_duckdb function
    init_duckdb(df, table_name, database_directory)