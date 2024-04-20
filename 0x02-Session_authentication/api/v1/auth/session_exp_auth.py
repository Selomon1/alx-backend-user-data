#!/usr/bin/env python3
"""
Module
"""

from flask import request
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for session expiration authentication
    """
    def __init__(self):
        """Initializa SessionExpAuth instance"""
        super().__init__()
        session_duration_str = getenv("SESSION_DURATION", "0")
        self.session_duration = int(session_duration_str) if session_duration_str.isdigit() else 0

    def create_session(self, user_id=None):
        """
        Create a session for a user
        Args:
            user_id (str): The user ID
        Returns:
            str: The session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            if session_id not in self.user_id_by_session_id:
                self.user_id_by_session_id[session_id] = {}
            self.user_id_by_session_id[session_id]['user_id'] = user_id
            self.user_id_by_session_id[session_id]['created_at'] = datetime.now()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Get the user ID for a given session ID
        Args:
            session_id (str): The session ID
        Returns:
            str: The user ID or None if session is invalid or expired
        """
        if not session_id:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None
        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')
        if not user_id or not created_at:
            return None
        if self.session_duration <= 0:
            return user_id
        if (created_at + timedelta(seconds=self.session_duration)) <= datetime.now():
            return None
        return user_id
