import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('spx.db')
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Flag to indicate if any missing values are found
missing_values_found = False

# Iterate over tables
for table in tables:
    table_name = table[0]

    # Read data into pandas DataFrame
    query = f"SELECT * FROM \"{table_name}\""
    df = pd.read_sql(query, conn)

    # Check for missing data
    missing_data_count = df.isna().sum().sum()  # Total missing values in the table

    if missing_data_count > 0:
        print(f"Table {table_name} has {missing_data_count} missing data points.")
        missing_values_found = True

if not missing_values_found:
    print("No tables with missing data found.")

# Close the connection
conn.close()
