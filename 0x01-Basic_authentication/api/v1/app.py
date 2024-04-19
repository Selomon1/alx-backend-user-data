#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Error handler for 401 Unauthorized.
    Args:
        error: the error message.
    Returns:
        A JSON response with status code 401.
    """
    return jsonify({"errpr": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Error handler for 403 Forbidden.
    Args:
        error: the error message.
    Returns:
        A JSON response with status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    excluded_paths = ['/api/v1/status/',
                      'api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth is None or request.path in excluded_paths:
        return
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
