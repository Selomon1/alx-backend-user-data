#!/usr/bin/env python3

"""
Module that defines the Flask application
"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(401)
def unauthorized(error):
    """
    Error handler for 401 Unauthorized status code
    Returns:
        A JSON response with the error message.
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(error):
    response = jsonify({'error': 'Forbidden'})
    response.status_code = 403
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
