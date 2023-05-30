#!/usr/bin/env python3.8
'''
File: auth.py
'''

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Class Auth to manage API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        """
        return None
