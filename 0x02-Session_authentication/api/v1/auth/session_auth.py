#!/usr/bin/env python3
"""
Module that manage session Authentication
"""

from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User
import os


class SessionAuth(Auth):
    """
    Class for managing session authentication
    Attributes:
        user_id_by_session_id (dict): Dictionary mapping session IDs to userID
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a given user ID
        Args:
            user-id (str); the user ID
        Returns:
            str: The session ID generated, else none
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID associated with a given session ID
        Args:
            session_id (str): The session ID for the user ID retrieved
        Returns:
            str: The user ID associated with session ID, else None
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the current user based on the session ID.
        Args:
            request: the request object contain the session ID
        Return:
            User: the user object correspond to the current session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """
        Delete the user session / logout
        Args:
            request: The request object
        Returns:
            bool: True if successfully destroyed, else False
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
