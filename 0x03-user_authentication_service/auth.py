#!/usr/bin/env python3
"""

HashPassword

"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
       >> Hash pasword using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """
       >> Generates a new UUID string.
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """
           >> Get Session ID.
        """
        try:
            user = self._db.find_user_by(email=email)   # find the user email
            session_id = _generate_uuid()  # Generate a new UUID for session ID
            user.session_id = session_id  # Set the session ID for the user
            self._db._session.commit()  # Commit changes to the database
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
           >> Retrieves user from session ID.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
            >> Destroy session for the user with the given user_id.
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
