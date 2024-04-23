#!/usr/bin/env python3
"""

Session Authentication

"""


from .auth import Auth


class SessionAuth(Auth):
    """
       >> A class that creates a new authentication mechanism.
       >> Validates if everything inherits correctly without any overloading.
       >> Validates the “switch” by using environment variables.
    """
    pass
