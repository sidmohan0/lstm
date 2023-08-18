import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('spx.db')
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over tables
for table in tables:
    table_name = table[0]

    # Read data into pandas DataFrame
    query = f"SELECT * FROM \"{table_name}\""
    df = pd.read_sql(query, conn)

    # Calculate daily returns based on the 'c' column (closing price)
    df['returns'] = df['c'].pct_change() * 100
    df = df.dropna(subset=['returns'])

    # Update the database with the new data
    # You can either update the existing table or create a new one
    # Here, we're replacing the existing table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f"Updated table {table_name} with daily returns.")

# Close the connection
conn.close()
