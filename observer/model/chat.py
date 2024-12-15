from typing import List
from uuid import uuid4
from observer.model.authentication import AuthenticatedAccount
from observer.manager.event_socket import EventManager, EventSendMessage


class Account:

    def __init__(self, username: str, password: str) -> None:
        self.authenticated = AuthenticatedAccount(username=username, password=password)


class Chat:

    __id_chat = uuid4().hex
    __sock_event = EventManager()

    def __init__(self) -> None:
        self.users: List[Account] = []

    def joined_chat(self, user: Account):
        for u in self.users:
            if u == user:
                raise Exception("usuario ya existente.")
        self.users.append(user)
        self.__sock_event.add_event(EventSendMessage())
        self.__sock_event.notify()

    def left_chat(self, user: Account):
        self.users.remove(user)

    @property
    def id_chat(self):
        return self.__id_chat
