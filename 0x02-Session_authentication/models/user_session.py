#!/usr/bin/env python3
"""
Module
"""

from sqlalchemy import Column, String
from models.base import Base


class UserSession(Base):
    """ Model for storing user sessions """
    __tablename__ = 'user_sessions'

    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
