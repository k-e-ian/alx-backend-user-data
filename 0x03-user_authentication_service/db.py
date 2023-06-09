#!/usr/bin/env python3.8
'''
File: db.py
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database

        Args:
            email (str): User's email
            hashed_password (str): User's hashed password

        Returns:
            User: User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the given filters
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found with the given filters")
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("Wrong query arguments") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """locate the user to update, then will update the user’s attributes
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid user attribute: {key}")
        self._session.commit()
