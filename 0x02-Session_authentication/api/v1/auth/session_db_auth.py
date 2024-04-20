#!/usr/bin/env python3
"""
Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    Session authentication using database
    """

    def __init__(self):
        """ Initialize SessionDBAuth """
        super().__init__()
        self.database_url = getenv('DATABASE_URL', '')
        self.engine = create_engine(self.database_url)

    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        if user_id:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            new_session = UserSession(
                user_id=user_id,
                session_id=super().create_session(user_id)
            )
            session.add(new_session)
            session.commit
            session.close()
            return new_session.session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user id from the database for a given session """
        if session_id:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            user_session = session.query(UserSession)\
                .filter_by(session_id=session_id).first()
            if user_session:
                user_id = super().user_id_for_session_id(session_id)
                session.close()
                return user_id
            session.close()
        return None

    def destroy_session(self, request=None):
        """ Destroy the session stored in the database """
        if request:
            session_id = self.session-cookie(request)
            if session_id:
                Session = sessionmaker(bind=self.engine)
                session = Session()
                user_session = session.query(UserSession)\
                    .filter_by(session_id=session_id).first()
                if user_session:
                    session.delete(user_session)
                    session.commit()
                session.close()
