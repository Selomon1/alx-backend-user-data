#!/usr/bin/env python3
"""
Module for encrypting passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The salted and hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password aganist a hashed password using bcrypt.
    Args:
        hashed_password (bytes): The hashed password to be validated
        password (str): the password to be validated.
    Returns:
        bool: True if the password matches the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
