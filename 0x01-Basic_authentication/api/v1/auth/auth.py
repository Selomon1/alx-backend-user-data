#!/usr/bin/env python3
"""
Module for managing API authentication.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Class to manage API authentication.
    """


    def require_auth(self, path: str, excluded_paths; List[str}) -> bool:
        """
        Method to check if authentication is required for given path.
        Always return False
        """


    def authorization_header9self, request=None) -> str:
        """
        Method to retrieve the authorization header from the request.
        Always returns None.
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user from the request.
        Always returns None.
        """
        return None
