#!/usr/bin/env python3
"""

API Authentication

"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
        >> Manages API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            >> Does the current path require authentication.
        """
        return False  # "path and excluded_paths" to be used later.

    def authorization_header(self, request=None) -> str:
        """
            >> Retrieve the authorization header from a request object.
        """
        return None  # "request" will be the Flask request object

    def current_user(self, request=None) -> TypeVar('User'):
        """
            >> Get the current user from the request.
        """
        return None  # "request" will be the Flask request object
