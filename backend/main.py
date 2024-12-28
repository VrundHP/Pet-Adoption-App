"""
This is the main application module that initializes the Flask app and defines routes
for user registration, login, pet management, application status, and user favorites.
"""

import sqlite3
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS

# Local imports
from user import register_user, login_user
from pets import add_pet, edit_pet
from application_status import get_application_status
from favorites import add_favorite, remove_favorite
from database import initialize_database

# Initialize database
initialize_database()

# Initialize Flask app
app = Flask(__name__)

CORS(app)  # Enable CORS
# Set up Swagger for API documentation
swagger = Swagger(app)


@app.route('/pets', methods=['GET'])
def get_pets():
    """
    Retrieves all pets from the database and returns them as JSON.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            SELECT name, age, breed, status, type, picture_url, location
            FROM pets
            '''
        )
        pets = cursor.fetchall()

        pet_data = [
            {
                "name": pet[0],
                "age": pet[1],
                "breed": pet[2],
                "status": pet[3],
                "type": pet[4],
                "picture_url": pet[5],
                "location": pet[6],
            }
            for pet in pets
        ]

        return jsonify({"pets": pet_data}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        conn.close()


# User routes
app.route('/register', methods=['POST'])(register_user)
app.route('/login', methods=['POST'])(login_user)

# Pet routes
app.route('/pets', methods=['POST'])(add_pet)  # Admin-only: Add a new pet


@app.route('/pets', methods=['DELETE'])
def remove_pet():
    """
    Removes a pet from the database based on its name and location.
    """
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return jsonify({"message": "Pet name and location are required"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'DELETE FROM pets WHERE name = ? AND location = ?',
            (name, location)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Pet not found"}), 404

        return jsonify({"message": "Pet removed successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        conn.close()


app.route('/pets', methods=['PUT'])(edit_pet)  # Admin-only: Edit a pet's details

# Application status route
app.route('/status', methods=['GET'])(get_application_status)

# Favorites routes
app.route('/favorites', methods=['DELETE'])(remove_favorite)
app.route('/favorites', methods=['POST'])(add_favorite)


@app.route('/favorites', methods=['GET'])
def get_favorites():
    """
    Retrieves a user's favorite pets based on their email.
    """
    email = request.args.get('email')  # Get email from query parameters
    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # Fetch user ID
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user[0]

        # Fetch user's favorite pet names
        cursor.execute('SELECT pet_name FROM favorites WHERE user_id = ?', (user_id,))
        favorite_pets = cursor.fetchall()

        if not favorite_pets:
            return jsonify({"favorites": []}), 200

        # Collect detailed pet information
        pets = []
        for (pet_name,) in favorite_pets:
            cursor.execute(
                '''
                SELECT name, age, breed, status, type, picture_url, location
                FROM pets
                WHERE name = ?
                ''',
                (pet_name,),
            )
            pet = cursor.fetchone()
            if pet:
                pets.append({
                    "name": pet[0],
                    "age": pet[1],
                    "breed": pet[2],
                    "status": pet[3],
                    "type": pet[4],
                    "picture_url": pet[5],
                    "location": pet[6],
                })

        return jsonify({"favorites": pets}), 200

    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        conn.close()

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
