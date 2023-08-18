import sqlite3
import os
import dotenv
from dotenv import load_dotenv

load_dotenv() # to get DB_PATH from .env file

# Connect to the SQLite database
conn = sqlite3.connect(os.environ.get('DB_PATH'))
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over tables and print details
# ...

# Iterate over tables and print details
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")

    # Get column information
    cursor.execute(f'PRAGMA table_info("{table_name}");')  # Use double quotes around table name
    columns = cursor.fetchall()

    # Print column name and data type
    for column in columns:
        col_name = column[1]
        col_type = column[2]
        print(f"  Column: {col_name} - Type: {col_type}")

# ...


# Close the connection
conn.close()


