#!/usr/bin/env python3
"""Auth module provides classes and functions for user authentication."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import TypeVar, Union


def _hash_password(password: str) -> bytes:
    """
    Generate a salted hash of the input password using bcrypt.

    Args:
        password (str): The password string to hash.
    Returns:
        bytes: The salted hash of the input password.
    """
    password_bytes = password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password


def _generate_uuid() -> str:
    """Genrate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The wemail of the user.
            password (str): the password of the user.
        Returns:
            User: the User object represent the newly registered.
        Raises:
            ValueError: if the user already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)

        user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Create a session for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session ID."""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user if user else None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session for user."""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user with given email.

        Args:
            email (str): The email of th user.
        Returns:
            str: the reset password token.
        Raises:
            ValueError: if no user found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update-user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User with email '{}' not found.".format(email))

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Update user's password using reset token.

        Args:
            reset-token (str): the reset token used to identify the user.
            new_password (str): the new password to be set for the user.
        Raises:
            ValueError: if the reset token is invalid or user not found.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(new_password)
            user.hashed_password = hashed_password
            user.rest_token = None
            self._db.commit()
        except noResultFound:
            raise ValueError("Invalid reset token")
