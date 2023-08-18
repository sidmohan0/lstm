import math
from polygon import RESTClient
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import datetime
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from sys import argv
import sqlite3
import requests
import yfinance as yf
import bs4 as bs
import pickle




load_dotenv() # to grab polygon.io API key from .env file

# API endpoint
# for the ticker symbol, we are actually going to use the S&P 500 index list of tickers
ticker = ''  # Stock ticker symbol
start_date = '2013-08-15' # Start date for data retrieval
end_date = '2023-08-15' # End date for data retrieval
limit = 5000 # Maximum number of data points to retrieve
timeframe = 'day' # Minute, hour, day, week, month, quarter, year
unadjusted = False # Stock splits and dividends will not be adjusted
sort = 'asc' # Sort chronologically (ascending or descending)
multiplier = 1 # Adjusts the time window (1, 2, 3, 4, 5, 10, 15, 30, 60)

# Construct API call from parameters
url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timeframe}/{start_date}/{end_date}?adjusted={unadjusted}&sort={sort}&limit={limit}&apiKey={os.environ.get('POLYGON_API_KEY')}"



# Make API call

# We are going to iterate through the list of tickers and make an API call for each ticker
# We will then store the data in a SQLite database

# Load S&P 500 Tickers

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('.', '-')
        ticker = ticker[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

save_sp500_tickers()
with open("sp500tickers.pickle", "rb") as f:
    tickers = pickle.load(f)
    print(len(tickers))  # Fixed the count method to len

    conn = sqlite3.connect('spx.db')  # Connecting to the database outside the loop

    for ticker in tickers:
        try:
            # Construct the API URL
            url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timeframe}/{start_date}/{end_date}?adjusted={unadjusted}&sort={sort}&limit={limit}&apiKey={os.environ.get('POLYGON_API_KEY')}"

            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()

                # Convert to pandas DataFrame
                df = pd.DataFrame(data_json['results'])

                # Connect to SQLite database
                conn = sqlite3.connect('spx.db')

                # Check if the table exists
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ticker}';")
                if cursor.fetchone() is None:
                    # Create table if it doesn't exist
                    # The exact query depends on the structure of your DataFrame
                    # Here, we're using pandas to create the table with the correct schema
                    df.to_sql(f'{ticker}', conn, if_exists='fail')
                    print(f"Table for {ticker} created.")
                else:
                    # Append to existing table
                    df.to_sql(f'{ticker}', conn, if_exists='append')
                    print(f'Data for {ticker} stored in SQLite database successfully.')

            else:
                print(f"Failed to retrieve data from API for {ticker}.")

        except Exception as e:
            print(f"An error occurred while processing {ticker}: {str(e)}")


    conn.close()  # Close the connection


# # print(values)
