#!/usr/bin/env python3
"""
Handles Session Authentication
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles POST request to authenticate users using session
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    new_session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), new_session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Logout the user (destroy the session)
    Returns:
        JSON: an empty JSON dictionary
    Raises:
        404: if the session canot be destroyed
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
