#!/usr/bin/env python3
"""Module contains end to end interaction with the authentication."""

import requests
from app import AUTH

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user with email and password.

    Args:
        email (str): the email address of the user.
        password (str): the password of the user.
    """
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to login with the provided email and password expects to fail.

    Args:
        email (str): the email of the user.
        password (str): password of the user.
    """
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Tests behavior of trying to retrieve inf while being logged out."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests retrieving profile info while logged in."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    payload = response.json()
    email_from_payload = payload.get("email")
    user = AUTH.get_user_from_session_id(session_id)
    email_from_user = user.email
    assert email_from_payload == email_from_user


def log_out(session_id: str) -> None:
    """Logs out a user session.

    Args:
        session_id (str): the session ID of the userto log out.

    Raises:
        AssertionError: if the logout process fails.
    """
    url = f"{BASE_URL}/sessions"
    headers = {"Content-Type": "application/json"}
    data = {"session_id": session_id}
    response = requests.delete(url, headers=headers, cookies=data)
    assert response.status_code == 200, "Failed to log out"


def reset_password_token(email: str) -> str:
    """Requests a password reset token for a given email.

    Args:
        email (str): the email address for which to request a reset.

    Returns:
        str: the reset token.

    Raises:
        AssertionError: if the reset token request fails.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, "Failed to reset password token"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates a user's password.

    Args:
        email (str): the user's email address.
        reset-token (str): the reset token for passwd reset
        new_password (str): the new password to set.

    Raises:
        AssertionError: if passwd update fails.
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200, "Failed to update password"
    assert (
        response.json()["message"] == "Password updated"
    ), "Password update failed"
    assert (
        response.json()["email"] == email
    ), "Email mismatch after password update"


def log_in(email: str, password: str) -> str:
    """Logs a user in by sending a POST request.

    Args:
        email (str): the email address
        password (str): the password of the user.

    Raises:
        ValueError: if the credentials invalid.

    Returns:
        str: the session ID of the logged in user.
    """
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 401:
        raise ValueError("Invalid credentials")
    assert response.status_code == 200, "Failed to log in"
    response_json = response.json()
    assert (
        "email" in response_json and
        "message" in response_json
    ), "Invalid response format"
    assert response_json["email"] == email, "Email mismatch in login response"
    return response.cookies.get("session_id")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
