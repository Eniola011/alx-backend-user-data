#!/usr/bin/env python3
"""

Password Encryption

"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
        >> User passwords should NEVER be stored in plain text in a database.
        >> Returns a salted, hashed password, which is a byte string.
    """
    encrypt = password.encode()
    hash_pwd = bcrypt.hashpw(encrypt, bcrypt.gensalt())
    return hash_pwd
