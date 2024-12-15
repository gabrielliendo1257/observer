from __future__ import annotations
from abc import ABC, abstractmethod
from socketserver import BaseRequestHandler
from typing import Any, List, Tuple
from observer.socks.configurations import TCP_Sock_Handler_Settings


class Decision(ABC):

    data: bytes = b""
    message: str = ""
    __request: Tuple[Any] = None

    @classmethod
    def set_request(cls, request):
        cls.__request = request

    @classmethod
    def get_request(cls):
        return cls.__request

    @abstractmethod
    def action(self): ...


class ReceiveMessage(Decision):

    def action(self):
        self.message = str(
            Decision.get_request().recv(
                TCP_Sock_Handler_Settings.recv_timeout_buffer_size
            )
        )
        print(self.message)


class SenderMessage(Decision):

    def action(self):
        Decision.get_request().sendall(self.data)


class ThreadedTcpRequestHandler(BaseRequestHandler):

    __decision: Decision = None
    __active_conections: List[Any] = []

    def handle(self) -> None:
        self.__active_conections.append(self.request)
        print(self.__active_conections)
        ThreadedTcpRequestHandler.get_decision().action()

    @classmethod
    def decision(cls, decision: Decision):
        cls.__decision = decision
        return cls.__decision

    @classmethod
    def get_decision(cls):
        return cls.__decision
