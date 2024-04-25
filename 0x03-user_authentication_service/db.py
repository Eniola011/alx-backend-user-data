#!/usr/bin/env python3
"""

DataBase Module.

"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """
       >> DataBase Class.
    """

    def __init__(self) -> None:
        """
           >> Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
           >> Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
           >> Adds and saves user to database.
           >> Return user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
           >> Takes in arbitrary keyword arguments and returns the first row
              found in the users table as filtered by the method’s
              input arguments.
           >> No validation of input arguments required at this point.
        """
        if kwargs is None:
            raise InvalidRequestError
        find_user = self._session.query(User).filter_by(**kwargs).first()
        if find_user is None:
            raise NoResultFound
        return find_user
