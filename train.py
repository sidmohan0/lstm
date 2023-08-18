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


# Connect to the SQLite database
conn = sqlite3.connect('spx.db')
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over tables
# Iterate over tables
for table in tables:
    table_name = table[0]

    # Query to get the most recent close price from the 'c' column
    query_recent_close = f"SELECT \"c\" FROM \"{table_name}\" ORDER BY ROWID DESC LIMIT 1"
    most_recent_close_price = cursor.execute(query_recent_close).fetchone()[0]

    # Check if the most recent close price is above $20
    if most_recent_close_price > 20:
        # Query to select all data from the table
        query = f"SELECT * FROM \"{table_name}\""
        df = pd.read_sql(query, conn)

        # ML analysis code goes here
        # ...
        print(f"Analyzing table {table_name} with most recent close price of ${most_recent_close_price:.2f}.")
    
        values = df['returns'].values # Get values from returns column

        training_data_len = math.ceil(len(values)* 0.8)
        # print(training_data_len)
    # Calculate daily returns and drop NaN values

    # print(df.head())


        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(values.reshape(-1,1))
        train_data = scaled_data[0: training_data_len, :]

        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
            
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))


        # Prepare Testing Data
        test_data = scaled_data[training_data_len-60: , : ]
        x_test = []
        y_test = values[training_data_len:]

        for i in range(60, len(test_data)):
            x_test.append(values[i-60:i, 0])

            x_test = np.array(x_test) 
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)) # Reshape the data



        model = keras.Sequential()
        model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(layers.LSTM(100, return_sequences=False))
        model.add(layers.Dense(25))
        model.add(layers.Dense(1))
        model.summary()

        # Set Optimizer and Loss Function
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size= 1, epochs=4)