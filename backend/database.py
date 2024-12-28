"""
This module handles database initialization and connection setup for the application.

It defines:
- A function to get a database connection (`get_db_connection`).
- A function to initialize the database (`initialize_database`), which sets up the schema
  for users, pets, favorites, questionnaires, and adoption applications.

Default data for pets is also inserted during initialization.
"""

import sqlite3

DATABASE = 'database.db'


def get_db_connection():
    """Initializes the database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initializes the database by creating required tables and inserting default data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

    # Drop existing tables for a clean slate
    print("Dropping existing tables...")
    cursor.execute('DROP TABLE IF EXISTS favorites')
    cursor.execute('DROP TABLE IF EXISTS pets')
    cursor.execute('DROP TABLE IF EXISTS users')

      # Create tables
    print("Creating tables...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create tables
    print("Creating tables...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT,
            address TEXT,
            background_check_status TEXT NOT NULL DEFAULT 'pending',
            profile_status TEXT NOT NULL DEFAULT 'active'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            description TEXT NOT NULL,
            breed TEXT NOT NULL,
            picture_url TEXT,
            status TEXT NOT NULL DEFAULT 'available',
            type TEXT NOT NULL,
            location TEXT NOT NULL,
            PRIMARY KEY (name, location) -- Enforce unique name/location combinations
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pet_name TEXT NOT NULL,
            pet_location TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (pet_name, pet_location) REFERENCES pets(name, location) ON DELETE CASCADE,
            UNIQUE(user_id, pet_name, pet_location) -- Prevent duplicate favorites for the same user and pet
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questionnaires (
            questionnaire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            submission_date DATE,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adoption_applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pet_name TEXT NOT NULL,
            location TEXT NOT NULL,
            submission_date DATE,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    # Insert default pets into the pets table
    print("Inserting default pets...")
    cursor.execute('''
        INSERT OR IGNORE INTO pets (name, age, description, breed, status, type, picture_url, location)
        VALUES 
        ('Jay', '1', 'Golden Lab', 'Lab', 'available', 'dog', '/jay.jpg', 'Hartford, CT'),
        ('Bella', '3', 'Playful and energetic', 'Golden Retriever', 'available', 'dog', '/bella.jpg', 'New Haven, CT'),
        ('Max', '2', 'Loves cuddles and naps', 'Beagle', 'available', 'dog', '/max.jpg', 'Stamford, CT'),
        ('Luna', '4', 'Quiet and friendly', 'Persian', 'available', 'cat', '/luna.jpg', 'Norwich, CT'),
        ('Rocky', '5', 'Very protective', 'German Shepherd', 'available', 'dog', '/rocky.jpg', 'Danbury, CT'),
        ('Mittens', '1', 'Loves climbing and exploring', 'Tabby', 'available', 'cat', '/mittens.jpg', 'Waterbury, CT')
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
