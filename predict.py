
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






# Run Predictions
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Calculate RMSE
rmse= np.sqrt(np.mean((predictions - y_test)**2))
rmse
print(rmse)

