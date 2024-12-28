"""
This module contains tests for the favorites API endpoints, including adding and retrieving
favorite pets for a user.
"""

import pytest
import logging
import sys
import os

# Add the parent directory to sys.path so we can import from the /backend folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database import initialize_database  # Import from /backend/database.py
from main import app  # Import Flask app from /backend/main.py

@pytest.fixture
def client():
    """
    Set up the Client in each test file.
    """
    # Remove existing database to start fresh
    if os.path.exists("database.db"):
        os.remove("database.db")

    # Initialize a fresh database with test data
    initialize_database()

    # Check if the database was created successfully
    if os.path.exists("database.db"):
        logging.info("Database file 'database.db' created successfully.")
    else:
        logging.error("Database file 'database.db' was not created.")
    
    with app.test_client() as client:
        yield client


def test_add_favorite(client):
    """
    Tests the /favorites POST endpoint by adding favorite pets and handling cases with missing data.
    """
    # Register the user `testuser`
    client.post("/register", json={"username": "testuser", "password": "password", "email": "testuser@example.com"})

    # Add a pet
    client.post("/pets", json={
        "name": "Buddy", "age": "2", "description": "Golden Retriever",
        "breed": "Golden Retriever", "picture_url": "/buddy.jpg",
        "status": "available", "type": "dog", "location": "Hartford, CT"
    })

    # Add the pet to favorites
    response = client.post("/favorites", json={"email": "testuser@example.com", "pet_name": "Buddy"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Pet added to favorites"}

    # Test missing data case
    response = client.post("/favorites", json={"email": "testuser@example.com"})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Email and Pet Name are required"}


def test_get_favorites(client):
    """
    Tests the /favorites GET endpoint by retrieving favorite pets for a user and handling cases
    with missing or empty data.
    """
    # Register the user `testuser`
    client.post("/register", json={"username": "testuser", "password": "password", "email": "testuser@example.com"})

    # Add a pet
    client.post("/pets", json={
        "name": "Buddy", "age": "2", "description": "Golden Retriever",
        "breed": "Golden Retriever", "picture_url": "/buddy.jpg",
        "status": "available", "type": "dog", "location": "Hartford, CT"
    })

    # Add the pet to favorites
    client.post("/favorites", json={"email": "testuser@example.com", "pet_name": "Buddy"})

    # Expected favorites with pet details for `testuser`
    expected_favorites = [
        {
            "name": "Buddy",
            "age": "2",
            "breed": "Golden Retriever",
            "picture_url": "/buddy.jpg",
            "status": "available",
            "type": "dog",
            "location": "Hartford, CT"
        }
    ]

    # Test retrieving favorites list for `testuser`
    response = client.get("/favorites", query_string={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.get_json() == {"favorites": expected_favorites}
