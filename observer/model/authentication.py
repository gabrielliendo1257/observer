from security.auth.base import User


class AuthenticatedAccount(User):

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class NotAuthenticatedAccount(User):

    def __init__(self) -> None:
        self.username = "random"
        self.password = None


class Administrator(User):

    def __init__(self) -> None:
        self.username = "admin"
        self.password = "admin"
