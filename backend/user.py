"""
This module provides user registration and login functionality using SQLite and mock checks.
"""

from flask import jsonify
from utils import get_json_data, connect_to_database


def register_user():
    """
    Registers a new user with a username, password, and email.

    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The user's desired username.
              example: "johndoe"
            password:
              type: string
              description: The user's chosen password.
              example: "securepassword123"
            email:
              type: string
              description: The user's email address.
              example: "johndoe@example.com"
    responses:
      200:
        description: User registered successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User 'johndoe' registered successfully"
      400:
        description: Username or email already exists or missing fields.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Username or email already exists"
      401:
        description: Background check failed.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Background check failed"
    """
    data, error = get_json_data(required_fields=["username", "password", "email"])
    if error:
        return jsonify({"message": error}), 400

    conn, cursor = connect_to_database()
    cursor.execute(
    'SELECT user_id FROM users WHERE username = ? OR email = ?',
    (data["username"], data["email"])
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "Username or email already exists"}), 400

    # Mock background check
    background_check_passed = True
    if background_check_passed:
        cursor.execute(
            '''INSERT INTO users (username, password, email) VALUES (?, ?, ?)''',
            (data["username"], data["password"], data["email"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": f"User '{data['username']}' registered successfully"}), 200

    conn.close()
    return jsonify({"message": "Background check failed"}), 401


def login_user():
    """
    Authenticates a user by verifying the username and password in the SQLite database.

    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username of the user attempting to log in.
              example: "johndoe"
            password:
              type: string
              description: The password of the user attempting to log in.
              example: "securepassword123"
    responses:
      200:
        description: Login successful.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Login successful"
      400:
        description: Missing required fields.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Username and password are required"
      401:
        description: Invalid credentials or authentication failed.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Invalid credentials"
    """
    data, error = get_json_data(required_fields=["username", "password"])
    if error:
        return jsonify({"message": error}), 400

    conn, cursor = connect_to_database()
    cursor.execute('SELECT password FROM users WHERE username = ?', (data["username"],))
    user = cursor.fetchone()
    conn.close()

    if user and data["password"] == user[0]:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
