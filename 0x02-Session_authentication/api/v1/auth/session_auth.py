#!/usr/bin/env python3
"""

Session Authentication

"""


from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
       >> A class that creates a new authentication mechanism.
       >> Validates if everything inherits correctly without any overloading.
       >> Validates the “switch” by using environment variables.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
           >> Creates a Session ID for a user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
           >> Returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
        # Now you have 2 methods (create_session and user_id_for_session_id)..
        # for storing and retrieving a link between a User ID and a Session ID.

    def current_user(self, request=None):
        """
           >> Returns a User instance based on a cookie value.
        """
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        _my_session_id = self.user_id_for_session_id(session_cookie)
        return User.get(_my_session_id)

    def destroy_session(self, request=None):
        """
           >> Deletes the user session or logout.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(request)

        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
