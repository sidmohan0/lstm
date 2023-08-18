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






# Visualize Results
data = df.filter(['returns'])
train = data[:training_data_len]
validation = data[training_data_len:]
validation['Predictions'] = predictions
plt.figure(figsize=(1000,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Daily Returns')
plt.plot(train)
plt.plot(validation[['returns', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()


