#!/usr/bin/env python3
"""

Basic Auth

"""


from base64 import b64decode
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
        >> Inherits from Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """
            >> Returns the Base64 part of the Authorization header..
               for a Basic Authentication.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        auth_value = authorization_header.split(' ')
        return auth_value[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
            >> Returns the decoded value of a Base64 string..
               base64_authorization_header.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decode_base64 = b64decode(base64_bytes)
            value = decode_base64.decode('utf-8')
            return value
        except Exception:
            return None
