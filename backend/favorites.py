"""
Module: favorites
This module provides functions to add, retrieve, and remove a user's favorite pets.
"""

import sqlite3
from flask import request, jsonify

DATABASE = 'database.db'


def add_favorite():
    """
    Adds a new pet to a user's favorite pets using their email and the pet's name.
    """
    data = request.get_json()
    email = data.get("email")
    pet_name = data.get("pet_name")

    if not email or not pet_name:
        return jsonify({"message": "Email and Pet Name are required"}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get user ID by email
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "User not found"}), 404
        user_id = user[0]

        # Get pet location by name
        cursor.execute('SELECT location FROM pets WHERE name = ?', (pet_name,))
        pet = cursor.fetchone()
        if not pet:
            return jsonify({"message": "Pet not found"}), 404
        pet_location = pet[0]

        # Check if the pet is already in favorites
        cursor.execute(
            'SELECT * FROM favorites WHERE user_id = ? AND pet_name = ? AND pet_location = ?',
            (user_id, pet_name, pet_location)
        )
        if cursor.fetchone():
            return jsonify({"message": "This pet is already in your favorites"}), 409

        # Add to favorites
        cursor.execute(
            'INSERT INTO favorites (user_id, pet_name, pet_location) VALUES (?, ?, ?)',
            (user_id, pet_name, pet_location)
        )
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Pet added to favorites"}), 200


def remove_favorite():
    """
    Removes a pet from a user's favorite pets using their email and the pet's name.
    """
    data = request.get_json()
    email = data.get("email")
    pet_name = data.get("pet_name")

    if not email or not pet_name:
        return jsonify({"message": "Email and Pet Name are required"}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get user ID by email
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "User not found"}), 404
        user_id = user[0]

        # Remove from favorites
        cursor.execute(
            'DELETE FROM favorites WHERE user_id = ? AND pet_name = ?',
            (user_id, pet_name)
        )
        conn.commit()
        rows_deleted = cursor.rowcount
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    if rows_deleted == 0:
        return jsonify({"message": "Pet not found in favorites"}), 404

    return jsonify({"message": "Pet removed from favorites"}), 200


def get_favorites():
    """
    Retrieves a list of a user's favorite pets using their email.
    """
    email = request.args.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get user ID by email
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "User not found"}), 404
        user_id = user[0]

        # Retrieve favorite pets with all fields, including description
        cursor.execute('''
        SELECT pets.name, pets.age, pets.description, pets.breed, 
               pets.picture_url, pets.status, pets.type, pets.location
        FROM favorites
        JOIN pets ON favorites.pet_name = pets.name AND favorites.pet_location = pets.location
        WHERE favorites.user_id = ?
        ''', (user_id,))
        favorites = cursor.fetchall()

        favorite_pets = [
            {
                "name": pet[0],
                "age": pet[1],
                "description": pet[2],
                "breed": pet[3],
                "picture_url": pet[4],
                "status": pet[5],
                "type": pet[6],
                "location": pet[7],
            }
            for pet in favorites
        ]
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"favorites": favorite_pets}), 200
