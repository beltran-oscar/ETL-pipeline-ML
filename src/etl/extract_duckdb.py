# %% tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None

# %%
import requests
import pandas as pd
import os
import duckdb
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path



# %%

# Load API key from .env file
api_key = os.getenv('API_KEY')

def extract(api_key):
    """
    Fetch and process air quality measurements from the OpenAQ API.

    Parameters
    ----------
    api_key : str
        API key for authentication with the OpenAQ API.

    Returns
    -------
    df : pandas.DataFrame or None
        Dataframe containing the fetched measurements, or None if no data is fetched.
    """
    
    # API URL
    api_url = "https://api.openaq.org/v2/measurements"
    
    # Define the query parameters to API
    params = {
        "location_id": "380422",
        "parameter": ["pressure", "temperature", "um003", "um025", "um010", "pm10", "um100", "pm1", "um005", "humidity", "um050", "pm25"],
        "limit": 9000,
        "api_key": api_key
    }
    
    try:
        # Make the GET request
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        if response.status_code == 200:
            data = response.json()
            output = pd.json_normalize(data['results'])
            df = pd.DataFrame(output)
            
            if df.empty:
                print("Extracted dataframe is empty. No data to load.")
                return None

            df['date.utc'] = pd.to_datetime(df['date.utc'], errors='coerce')
            df['date.local'] = df['date.utc'].dt.tz_convert('America/Los_Angeles')
            df['date.local'] = df['date.local'].dt.tz_localize(None)
            df = df[df['value'] > 0.0]
            
            return df

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error: Something Else", err)

# %%


# Create local DuckDB instance
# Define table name
table_name = "air_data"

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
    try:
        duckdb_directory = os.path.join(database_directory, "air_data.duckdb")
        con = duckdb.connect(duckdb_directory)
        
        # Check if table already exists, if not, create it
        tables = con.execute("SHOW TABLES").fetchall()
        if table_name not in [table[0] for table in tables]:
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        
        con.close()
    except Exception as e:
        print(e)
        print(type(df))


# %%
def load_into_motherduck(df, md_token):
    """
    Load data from a pandas DataFrame into MotherDuck.

    Parameters
    ----------
    df : pandas.DataFrame or None
        DataFrame to be loaded into MotherDuck. If None, nothing is loaded.
    md_token : str
        The MotherDuck token.
    """

    if df is None:
        print("No data to load into MotherDuck.")
        return
    
    # Assert that 'md_token' is neither None nor empty, else raise an AssertionError.
    assert md_token and md_token.strip() != '', "MOTHERDUCK_TOKEN is not set or is empty."

    # Connect to MotherDuck database
    motherduck_con = duckdb.connect(f'md:?motherduck_token={md_token}')
    
    # Load the MotherDuck module.
    motherduck_con.execute("LOAD motherduck")
    
    # Uploads pandas datafarme into  MotherDuck database.
    motherduck_con.execute("CREATE OR REPLACE TABLE openaq_api.main.df as SELECT * FROM 'df'")
    
    # Close connection after dataframe is uploaded
    motherduck_con.close()



# %%
if __name__ == "__main__":
    # Load API key from .env file
    load_dotenv('.env')
    api_key = os.getenv('API_KEY')

    # Get MotherDuck token
    md_token = os.getenv('MOTHERDUCK_TOKEN')
    
    # Call extract function
    df = extract(api_key)
    print(type(df))

    # Define table name
    table_name = "air_data"

    # Define current working directory
    current_dir = os.getcwd()

    # Define directory to store DuckDB database
    database_directory = os.path.join(current_dir, "src", "data")

    # Call init_duckdb function
    init_duckdb(df, table_name, database_directory)

    # Call load_into_motherduck function
    load_into_motherduck(df, md_token)