#!/usr/bin/env python3
"""

HashPassword

"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
       >> Hash pasword using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


class Auth:
    """
       >> Auth class to interact with the authentication database.
    """
    def __init__(self):
        """
           >> Initialize Class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
           >> Register a new user and return user object.
        """
        # Check if a user with the provided email already exists.
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError('User {email} already exists')
        except NoResultFound:
            pass
        # hash the password.
        hash_pwd = _hash_password(password)
        # create and save the new user.
        new_user = self._db.add_user(email, hash_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
           >> Validates Login Credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False
