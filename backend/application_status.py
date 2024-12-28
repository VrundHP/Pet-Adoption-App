"""
Module: application_status
This module provides functions related to application status.
"""

import sqlite3
from flask import request, jsonify

DATABASE = 'database.db'

def get_db_connection():
    """Establishes a database connection and returns the connection object."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name
    return conn

def get_application_status():
    """
    Retrieves the status of an application from the database based on application_id or user_id.

    ---
    tags:
      - Application Status
    parameters:
      - name: application_id
        in: body
        required: false
        description: The ID of the application to retrieve the status for.
        schema:
          type: integer
      - name: user_id
        in: body
        required: false
        description: The ID of the user whose application status to retrieve.
        schema:
          type: integer
    responses:
      200:
        description: Successfully retrieved the application status.
        schema:
          type: object
          properties:
            application_id:
              type: integer
            user_id:
              type: integer
            pet_id:
              type: integer
            submission_date:
              type: string
              format: date
            status:
              type: string
              description: The current status of the application (e.g., "pending", "approved").
            decision_by_admin:
              type: string
              description: The decision made by the admin regarding the application.
      400:
        description: Bad request, application_id or user_id is required.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Application ID or User ID is required"
      404:
        description: Application not found based on the provided ID.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Application not found"
    """
    # Retrieve application ID or user ID from the request (assuming either can be provided)
    data = request.get_json()
    application_id = data.get("application_id")
    user_id = data.get("user_id")

    if not application_id and not user_id:
        return jsonify({"message": "Application ID or User ID is required"}), 400

    # Query the database for the application status
    conn = get_db_connection()
    cursor = conn.cursor()

    if application_id:
        cursor.execute(
            'SELECT * FROM adoption_applications WHERE application_id = ?', (application_id,)
        )
    else:
        cursor.execute(
            'SELECT * FROM adoption_applications WHERE user_id = ?', (user_id,)
        )

    application = cursor.fetchone()
    conn.close()

    if application:
        status = {
            "application_id": application["application_id"],
            "user_id": application["user_id"],
            "pet_id": application["pet_id"],
            "submission_date": application["submission_date"],
            "status": application["status"],
            "decision_by_admin": application["decision_by_admin"]
        }
        return jsonify(status), 200

    return jsonify({"message": "Application not found"}), 404
