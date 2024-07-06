import sqlite3

# Connect to a new (or existing) database file
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Example: Create a new table (optional)
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    hash VARCHAR(128) NOT NULL
);
''')

# Commit the changes (if any) and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
