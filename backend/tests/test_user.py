"""
This module contains tests for user registration and login endpoints.
"""

import json
from werkzeug.test import Client
import sys
import os
from dbfuncs import clear_and_reinitialize_database

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import your app from main.py
from main import app

# Set up the Test Client for the Flask app
client = app.test_client()  # Automatically handles the request environment

clear_and_reinitialize_database() # clear database first

def test_register_user():
    """
    Tests the /register endpoint with a mock user registration request that includes email.
    """
    response = client.post(
        '/register',
        data=json.dumps({
            "username": "testuser", 
            "password": "password123", 
            "email": "testuser@example.com"
        }),
        content_type='application/json'
    )

    print(f'\nStatus code of register_user\'s post request {response.status_code}\n')
    assert response.status_code == 200
    response_json = json.loads(response.data.decode())
    expected_message = "User 'testuser' registered successfully"
    assert response_json["message"] == expected_message

def test_already_exists():
    """
    Tests the /register endpoint with mock user registration requests, testing for username and email duplication.
    """

    # Try to register the same username again (should fail)
    response = client.post(
        '/register',
        data=json.dumps({
            "username": "testuser", 
            "password": "newpassword", 
            "email": "newemail@example.com"
        }),
        content_type='application/json'
    )
    print(response.status_code)
    assert response.status_code == 400

    # Try to register the same email again (should fail)
    response = client.post(
        '/register',
        data=json.dumps({
            "username": "newuser", 
            "password": "newpassword", 
            "email": "testuser@example.com"
        }),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_login_user():
    """
    Tests the /login endpoint with a mock user login request after registration.
    """
    # Register a user first
    client.post(
        '/register',
        data=json.dumps({
            "username": "testuser", 
            "password": "password123", 
            "email": "testuser@example.com"
        }),
        content_type='application/json'
    )

    # Now test logging in with the registered credentials
    response = client.post(
        '/login',
        data=json.dumps({
            "username": "testuser", 
            "password": "password123"
        }),
        content_type='application/json'
    )

    print(f'\nStatus code of login_user\'s post request {response.status_code}\n')
    assert response.status_code == 200
    assert json.loads(response.data.decode()) == {"message": "Login successful"}

def test_unsuccessful_login_username_not_found():
    """
    Tests the /login endpoint for an unsuccessful login where the username does not exist.
    """
    response = client.post(
        '/login',
        data=json.dumps({"username": "nonexistentuser", "password": "any_password"}),
        content_type='application/json'
    )
    assert response.status_code == 401
    assert json.loads(response.data.decode()) == {"message": "Invalid credentials"}

def test_unsuccessful_login_invalid_password():
    """
    Tests the /login endpoint for an unsuccessful login where the password is incorrect.
    """
    # Register a user first
    client.post(
        '/register',
        data=json.dumps({
            "username": "testuser", 
            "password": "password123", 
            "email": "testuser@example.com"
        }),
        content_type='application/json'
    )

    # Now test logging in with an incorrect password
    response = client.post(
        '/login',
        data=json.dumps({"username": "testuser", "password": "wrongpassword"}),
        content_type='application/json'
    )
    assert response.status_code == 401
    assert json.loads(response.data.decode()) == {"message": "Invalid credentials"}

if __name__ == "__main__":
    test_register_user()
    test_already_exists()
    test_login_user()
    test_unsuccessful_login_username_not_found()
    test_unsuccessful_login_invalid_password()
