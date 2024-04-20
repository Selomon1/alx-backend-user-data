#!/usr/bin/env python3
"""
Module
"""

from sqlalchemy import Column, String
from models.base import Base


class UserSession(Base):
    """ Model for storing user sessions """
    __tablename__ = 'user_sessions'

    user_id = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=False)

    def __init__(self, user_id=None, session_id=None):
        self.user_id = user_id
        self.session_id = session_id
