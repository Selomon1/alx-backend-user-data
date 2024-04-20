#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from typing import List, TypeVar
from re import search, sub
import os


class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Methods to determine if authentication is required for the path.
        Args:
            path: the path to check
            excluded_paths: List of paths excluded from auth.
        Returns:
            True if auth is required, else False.
        """
        if path is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if search(sub(r"\*", ".*", excluded_path), path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the authorization header from the request.
        Args:
            request: the Flask request object.
        Returns:
            The value of the Authorization header or None if not
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user.
        Args:
            request: the Flask request object.
        Returns:
            None for this placeholder implementation.
        """
        return None

    def session_cookie(self, request=None):
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
