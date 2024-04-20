#!/usr/bin/env python3
"""Module SessionDB Authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session database authentication class"""

    def create_session(self, user_id=None):
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_id = str(uuid.uuid4())
        user_session = UserSession(
            user_id=user_id,
            session_id=session_id
        )
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user id from the database for a given session"""
        if not session_id or not isinstance(session_id, str):
            return None

        user_session = UserSession.get(session_id)
        if not user_session:
            return None

        session_expiry = (
            user_session.created_at +
            timedelta(seconds=self.session_duration)
        )
        if session_expiry < datetime.utcnow():
            user_session.remove()
            return none

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the session stored in the database"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return false

        user_session = UserSession.get(session_id)
        user_sesssion.remove()

        return True
