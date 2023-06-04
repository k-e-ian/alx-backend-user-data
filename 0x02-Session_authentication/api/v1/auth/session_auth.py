#!/usr/bin/env python3.8
'''
File: session_auth.py
'''
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Class SessionAuth to manage API authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        create session method
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id