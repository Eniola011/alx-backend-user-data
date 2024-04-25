#!/usr/bin/env python3
"""

HashPassword

"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """
       >> Hash pasword using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd
