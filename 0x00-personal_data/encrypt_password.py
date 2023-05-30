#!/usr/bin/env python3.8
'''
File: encrypt_password.py
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
    Hashes and salts the password using bcrypt
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Validates if the provided password matches the hashed password
    '''
    return bcrypt.checkpw(password.encode(), hashed_password)
