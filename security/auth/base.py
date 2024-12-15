from __future__ import annotations
from abc import ABC, abstractmethod

from observer.model.authentication import NotAuthenticatedAccount


class User(ABC):
    __reference = None

    username = None
    password = None
    __is_blocket: bool = False

    def __new__(cls):
        if cls.__reference == None:
            cls.__reference = super().__new__(cls)
            return cls.__reference
        return cls.__reference

    @property
    def is_authenticated(self):
        if self.username != None and self.password != None:
            return True
        return False

    @property
    def blocket(self) -> bool:
        return self.__is_blocket

    @blocket.setter
    def blocket(self, user: User):
        if isinstance(user, NotAuthenticatedAccount):
            self.__is_blocket = True
        else:
            self.__is_blocket = False

    def authenticated(self): ...

    @classmethod
    def get_authenticated_account(cls):
        if not User.is_authenticated and User.blocket:
            raise
        return super().__new__(cls)

    def __eq__(self, user) -> bool:
        return self.username == user.username
