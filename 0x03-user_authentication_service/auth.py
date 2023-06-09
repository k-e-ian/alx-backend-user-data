#!/usr/bin/env python3.8
'''
File: auth.py
'''
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """method that takes in a password string args and returns bytes."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), s    alt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        takes mandatory email and pass str args and return a User object."""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = self._db._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password.encode('utf-8')
            password = password.encode('utf-8')
            if bcrypt.checkpw(password, hashed_password):
                return True
            else:
                raise InvalidPasswordError("Invalid password")
        except UserNotFoundError:
            return False
        except Exception as e:
            raise Exception("Error occurred during login validation") from e

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user."""
        user = self._db.find_user_by(email=email)
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID"""
        return str(uuid.uuid4())

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve the user corresponding to the provided session ID."""
        if session_id is None:
            return None

        user = self._db.get_user_by_session_id(session_id)
        return user if user else None
