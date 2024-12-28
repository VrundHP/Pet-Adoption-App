import json
import sys
import os
import pytest

# Add the parent directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database import initialize_database
from main import app

@pytest.fixture
def client():
    """Set up the Flask test client for each test."""
    if os.path.exists("database.db"):
        os.remove("database.db")
    initialize_database()
    with app.test_client() as client:
        yield client

def test_add_pet(client):
    response = client.post('/pets', data=json.dumps({
        "name": "Buddy", "age": "3", "description": "Playful and energetic",
        "breed": "Golden Retriever", "picture_url": "/buddy.jpg",
        "status": "available", "type": "dog", "location": "Hartford, CT"
    }), content_type='application/json')
    assert response.status_code == 201
    assert response.get_json() == {"message": "Pet added successfully"}

def test_add_pet_already_exists(client):
    client.post('/pets', data=json.dumps({
        "name": "Max", "age": "4", "description": "Friendly and playful",
        "breed": "German Shepherd", "picture_url": "/max.jpg",
        "status": "available", "type": "dog", "location": "Stamford, CT"
    }), content_type='application/json')
    response = client.post('/pets', data=json.dumps({
        "name": "Max", "age": "4", "description": "Friendly and playful",
        "breed": "German Shepherd", "picture_url": "/max.jpg",
        "status": "available", "type": "dog", "location": "Stamford, CT"
    }), content_type='application/json')
    assert response.status_code == 409
    assert response.get_json() == {"message": "Pet already exists"}

def test_remove_pet(client):
    client.post('/pets', data=json.dumps({
        "name": "Lucy", "age": "2", "description": "Loves to play fetch",
        "breed": "Labrador", "picture_url": "/lucy.jpg",
        "status": "available", "type": "dog", "location": "New Haven, CT"
    }), content_type='application/json')
    response = client.delete('/pets', data=json.dumps({"name": "Lucy", "location": "New Haven, CT"}), content_type='application/json')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Pet removed successfully"}

def test_remove_nonexistent_pet(client):
    response = client.delete('/pets', data=json.dumps({"name": "Nonexistent Pet", "location": "Unknown"}), content_type='application/json')
    assert response.status_code == 404
    assert response.get_json() == {"message": "Pet not found"}

def test_edit_pet(client):
    """
    Tests the /pets endpoint to edit a pet's details.
    """
    client.post('/pets', data=json.dumps({
        "name": "Bella", "age": "5", "description": "Friendly and calm",
        "breed": "Beagle", "picture_url": "/bella.jpg",
        "status": "available", "type": "dog", "location": "Danbury, CT"
    }), content_type='application/json')

    response = client.put('/pets', data=json.dumps({
        "name": "Bella", "location": "Danbury, CT",
        "age": "6", "description": "Loves long walks",
        "breed": "Beagle", "picture_url": "/bella_updated.jpg",
        "status": "adopted", "type": "dog"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.get_json() == {"message": "Pet details updated successfully"}

def test_edit_nonexistent_pet(client):
    response = client.put('/pets', data=json.dumps({
        "name": "Nonexistent Pet", "location": "Unknown",
        "age": "3", "description": "Does not exist",
        "breed": "Unknown", "picture_url": "/nonexistent.jpg",
        "status": "available", "type": "dog"
    }), content_type='application/json')
    assert response.status_code == 404
    assert response.get_json() == {"message": "Pet not found"}
