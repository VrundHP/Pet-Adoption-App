import sqlite3

def clear_and_reinitialize_database():
    """Clears all data by dropping tables and reinitializing the database."""
    # Connect to SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS pets')
    cursor.execute('DROP TABLE IF EXISTS favorites')

    # Reinitialize the users table with email column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )''')

    # Reinitialize the pets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        description TEXT,
        breed TEXT,
        picture_url TEXT,
        status TEXT NOT NULL DEFAULT 'available',
        type TEXT
    )''')

    # Reinitialize the favorites table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pet_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (pet_id) REFERENCES pets(pet_id)
    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database cleared and reinitialized successfully.")
