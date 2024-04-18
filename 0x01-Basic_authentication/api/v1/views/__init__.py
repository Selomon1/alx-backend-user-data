#!/usr/bin/env python3
"""
Package initializes the API version 1 views
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# import all views
from api.v1.views.index import *
