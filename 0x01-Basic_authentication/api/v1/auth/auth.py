#!/usr/bin/env python3
"""

API Authentication

"""


from flask import request
from typing import List, TypeVar, Optional


class Auth:
    """
        >> Manages API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            >> Does the current path require authentication.
            >> Args:
               > path (str): The path to evaluate.
               > excluded_paths (List[str]): A list of paths..
                 that do not require authentication.
            >> Returns:
               > bool: True if the path requires authentication.
                 false if otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        # method must be slash tolerant
        path = path + '/' if not path.endswith('/') else path
        # Check if the normalized path is in the list of excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            elif excluded_path.endswith('*'):
                base_path = excluded_path[:-1]
                if path.startswith(base_path):
                    return False
            else:
                if path == excluded_path + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
            >> Retrieve the authorization header from a request object.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            >> Get the current user from the request.
        """
        return None  # "request" will be the Flask request object
