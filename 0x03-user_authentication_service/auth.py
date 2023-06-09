#!/usr/bin/env python3.8
'''
File: auth.py
'''
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        takes mandatory email and pass str args and return a User object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = self._db._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
