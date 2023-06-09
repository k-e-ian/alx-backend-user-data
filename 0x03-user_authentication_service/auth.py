#!/usr/bin/env python3.8
'''
File: auth.py
'''
import bcrypt


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
