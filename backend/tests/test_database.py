import sqlite3
import pytest
import sys
import os

# Add the parent directory to sys.path so we can import from the /backend folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database import initialize_database  # Import from /backend/database.py

BASE_URL = "http://127.0.0.1:5001"

# Define the path to the database file
DB_PATH = 'database.db'

@pytest.fixture(scope="module")
def setup_database():
    """
    Pytest fixture to initialize the database and clean up after tests.
    This fixture runs once per module.
    """
    # Ensure the database is initialized
    initialize_database()
    yield

    # Clean up by removing the database file after tests are done
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_users_table_exists(setup_database):
    """Test that the users table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Users table should exist"

def test_admins_table_exists(setup_database):
    """Test that the admins table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admins'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Admins table should exist"

def test_pets_table_exists(setup_database):
    """Test that the pets table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pets'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Pets table should exist"

def test_favorites_table_exists(setup_database):
    """Test that the favorites table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='favorites'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Favorites table should exist"

def test_questionnaires_table_exists(setup_database):
    """Test that the questionnaires table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questionnaires'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Questionnaires table should exist"

def test_adoption_applications_table_exists(setup_database):
    """Test that the adoption_applications table is created successfully."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adoption_applications'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Adoption applications table should exist"
  
