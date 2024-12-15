from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from observer.socks.socket_server import ThreadedTcpRequestHandler
from security.auth.base import User


class EventManager:

    __listeners: List[EventSocket] = []

    def add_event(self, event: EventSocket):
        self.__listeners.append(event)
        print("Evento incluido: " + event.__class__.__name__)

    def delete_event(self, event: EventSocket):
        self.__listeners.remove(event)
        print("Evente eliminado: " + event.__class__.__name__)

    def notify(self):
        for event in self.__listeners:
            event.update()


class EventSocket(ABC):

    __user = User()

    @abstractmethod
    def update(self): ...


class EventSendMessage(EventSocket):

    def update(self):
        sock, addr = ThreadedTcpRequestHandler.request
        sock.sendall("Joined " + self.__user.username)


class EventReceiverMessage(EventSocket): ...


class EventUserDetected(EventSocket): ...
