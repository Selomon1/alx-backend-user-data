#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        Args:
            email (str): The email of the user.
            hashed_password (str): the hashed password of the user.
        Returns:
            User: The user object represent the newly added user.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.
        Args:
            **kwargs: arbitrary keyword arguments to filter users.
        Returns:
            User: the first user object matching the filter.
        Raises:
            NoResultFound: no user is founf matching the filter
            InvalidRequestError: wrong query.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attribute in the database
        Args:
            user_id (int): the ID of the user to update
            **kwargs: arbitrary keyword arguments torepresent user attribute
        Raises:
            ValueError: an invalid user attribute is provided.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User not found")

        for key in kwargs:
            if not hasattr(user, key):
                raise ValueError(f"Invalid user attribute: {key}")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
