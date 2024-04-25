#!/usr/bin/env python3
"""

Session Database Authentication.

"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """
       >> Session Database Authentication Class.
    """
    def __init__(self):
        """
           >> Initialize Class.
        """
        super().__init__()

    def create_session(self, user_id=None) -> str:
        """
           >> Create a new UserSession and return the Session ID.
        """
        session_id = str(uuid4())
        new_session = UserSession(user_id=user_id, session_id= session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
           >> Retrieve User ID from the database based on the Session ID.
        """
        if session_id is None:
            return None

        user_session = UserSession().find_first(session_id=session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id
        created_at = datetime.strptime(user_session.created_at,
                                       "%Y-%m-%d %H:%M:%S")
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            user_session.delete()
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
           >> Destroy the UserSession based on the Session ID from the request cookie.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = UserSession().find_first(session_id=session_id)
        if user_session is not None:
            user_session.delete()
            return True

        return False
