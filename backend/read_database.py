"""
Module: read_database.py
Used for fetching all data in database.db
"""

import sqlite3

DATABASE = 'database.db'

def read_table_data(table_name):
    """Reade and prints data from database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Access columns by name
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print(f"Data from {table_name}:")
        for row in rows:
            print(dict(row)) # Convert row to dictionary for easy reading
        print("\n" + "-"*30 + "\n")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    # Read from specific tables
    tables = ['users', 'admins', 'pets', 'favorites', 'questionnaires', 'adoption_applications']
    for table in tables:
        read_table_data(table)
