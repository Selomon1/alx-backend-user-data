#!/usr/bin/env python3
"""
Module that defines endpoints for API version1.
"""

from flask import abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'])
def unauthorized_endpoint():
    """
    Endpoint for testing unauthorized error (401)
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'])
def forbidden_route():
    abort(403)
