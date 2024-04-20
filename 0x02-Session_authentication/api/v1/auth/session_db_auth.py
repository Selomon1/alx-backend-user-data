#!/usr/bin/env python3
"""
Module SessionDB Authentication
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """
    Session database authentication class
    """

    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        session_id = super().create_session(user_id)
        if session_id:
            session_id = str(uuid.uuid4())
            new_session = UserSession(
                user_id=user_id,
                session_id=session_id)
            )
            new_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user id from the database for a given session """
        if session_id is None:
            return None
        user_session = UserSession.get(session_id)
        if user_session:
            return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """ Destroy the session stored in the database """
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.get(session_id)
            if user_session:
                user_session.delete()
        return None
