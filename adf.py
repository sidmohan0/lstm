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
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import sqlite3
import dotenv
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv() # to get DB_PATH from .env file

# Connect to the SQLite database
conn = sqlite3.connect(os.environ.get('DB_PATH'))
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# List to collect results
results = []

# List to collect tickers with stationary data
stationary_tickers = []

# Iterate over tables
for table in tables:
    table_name = table[0]

    # Read data into pandas DataFrame
    query = f"SELECT * FROM \"{table_name}\""
    df = pd.read_sql(query, conn)

    X = df["c"].values
    result = adfuller(X)

    # Check if the time series is stationary
    is_stationary = result[0] < result[4]["5%"]

    # Collect data points
    data_points = {
        "ticker": table_name,
        "ADF_Statistic": result[0],
        "p-value": result[1],
        "is_stationary": is_stationary
    }

    results.append(data_points)

    # If the time series is stationary, add the ticker to the list
    if is_stationary:
        stationary_tickers.append(table_name)

# Create DataFrame from results
results_df = pd.DataFrame(results)

# Write to CSV
results_df.to_csv('output.csv', index=False)

print("Results written to output.csv.")

# Print tickers with stationary data
if stationary_tickers:
    print("Tickers with stationary data:")
    print(", ".join(stationary_tickers))
else:
    print("No tickers with stationary data found.")