"""
This module provides pet-related functionalities using an SQLite database.
"""
import sqlite3
from flask import jsonify
from utils import get_json_data, connect_to_database


def add_pet():
    """
    Adds a new pet to the system.
    """
    data, error = get_json_data(
        required_fields=[
            "name", "age", "description", "breed", "picture_url", "type", "location"
        ]
    )
    if error:
        return jsonify({"message": error}), 400

    conn, cursor = connect_to_database()
    cursor.execute(
        'SELECT * FROM pets WHERE name = ? AND location = ?',
        (data["name"], data["location"])
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "Pet already exists"}), 409

    try:
        cursor.execute(
            '''
            INSERT INTO pets (name, age, description, breed, picture_url, 
                              status, type, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                data["name"], data["age"], data["description"], data["breed"],
                data["picture_url"], data.get("status", "available"),
                data["type"], data["location"]
            )
        )
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Pet added successfully"}), 201


def remove_pet():
    """
    Removes a pet from the system based on the pet's name and location.
    """
    data, error = get_json_data(required_fields=["name", "location"])
    if error:
        return jsonify({"message": error}), 400

    conn, cursor = connect_to_database()
    cursor.execute(
        'DELETE FROM pets WHERE name = ? AND location = ?',
        (data["name"], data["location"])
    )

    rows_deleted = cursor.rowcount
    if rows_deleted == 0:
        conn.close()
        return jsonify({"message": "Pet not found"}), 404

    conn.commit()
    conn.close()
    return jsonify({"message": "Pet removed successfully"}), 200


def edit_pet():
    """
    Edits an existing pet's details based on the pet's name and location.
    """
    data, error = get_json_data(
        required_fields=[
            "name", "location", "age", "description", "breed",
            "picture_url", "status", "type"
        ]
    )
    if error:
        return jsonify({"message": error}), 400

    conn, cursor = connect_to_database()
    try:
        # Verify the pet exists
        cursor.execute(
            'SELECT * FROM pets WHERE name = ? AND location = ?',
            (data["name"], data["location"])
        )
        if not cursor.fetchone():
            return jsonify({"message": "Pet not found"}), 404

        # Update pet details
        cursor.execute(
            '''
            UPDATE pets
            SET age = ?, description = ?, breed = ?, picture_url = ?, 
                status = ?, type = ?
            WHERE name = ? AND location = ?
            ''',
            (
                data["age"], data["description"], data["breed"],
                data["picture_url"], data["status"], data["type"],
                data["name"], data["location"]
            )
        )
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Pet details updated successfully"}), 200
