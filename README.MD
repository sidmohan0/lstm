# Overview

This python package is a collection of tools for analyzing stock data using Polygon.io's Stock API.  I collect tickers from the current list of S&P 500 companies and use the API to collect 10 yrs worth of daily candle data for each ticker.   

This is an entry point into my pipeline for further feature engineering and analysis using LSTM models for walk-forward predictions. 



# To-Do:

- Refactor code to remove redundancies (I split this out originally from monolithic script)
# Approach

## Data
Using Yfinance for testing and Polygon.io for production.



