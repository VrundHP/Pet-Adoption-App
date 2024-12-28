"""
Utility functions for common operations in the application.
"""

import sqlite3
from flask import request  # Removed unused jsonify import


def get_json_data(required_fields=None):
    """
    Retrieves and validates JSON data from the request.

    :param required_fields: A list of field names that must be present in the JSON data.
    :return: Tuple of (data, error_message). `data` is the parsed JSON object, 
             and `error_message` is None if all fields are valid.
    """
    data = request.get_json()

    if required_fields:
        # Check for missing fields
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            error_message = f"Missing fields: {', '.join(missing_fields)}"
            return None, error_message

    return data, None


def connect_to_database(db_name='database.db'):
    """
    Establishes a connection to the SQLite database.

    :param db_name: Name of the SQLite database file.
    :return: A tuple of (connection, cursor).
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor
