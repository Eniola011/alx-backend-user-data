#!/usr/bin/env python3
"""

Session Expiration Authentication.

"""


from api.v1.auth.session_auth import SessionAuth
from os import getenv
from uuid import uuid4
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
       >> Session Authentication with Expiration Class.
    """
    def __init__(self):
        """
           >> Initialize Class.
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_NAME', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
           >> Create a SessionID with Expiration.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        session_dictionary = {
            'user_id': user_id,
            'created_at': created_at
        }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
           >> Get User ID from Session ID with Expiration.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = datetime.strptime(session_dictionary.get('created_at'),
                                       "%Y-%m-%d %H:%M:%S")
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            del self.user_id_by_session_id[session_id]
            return None

        return session_dictionary.get('user_id')
