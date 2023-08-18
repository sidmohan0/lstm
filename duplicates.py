import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('spx.db')
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
# confirm number of tables
print(f"Number of tables: {len(tables)}")

# Iterate over tables
for table in tables:
    table_name = table[0]

    # Read data into pandas DataFrame
    query = f"SELECT * FROM \"{table_name}\""
    df = pd.read_sql(query, conn)

    # Remove duplicates in the 'd' column, keeping the first occurrence
    df_no_duplicates = df.drop_duplicates(subset=['t'], keep='first')

    # Update the database with the new data (replace existing table)
    df_no_duplicates.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f"Removed duplicates from table {table_name}.")


# Close the connection
conn.close()
print("Connection closed.")
