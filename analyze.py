import sqlite3

# Connect to the database
conn = sqlite3.connect('spx.db')

# Get the cursor
cursor = conn.cursor()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over tables and count rows
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    print(f"{table_name}: {row_count} rows")

# Close the connection
conn.close()
