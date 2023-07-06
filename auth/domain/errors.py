class AuthDomainError(Exception):
    ...


class EmailAlreadyExistsError(AuthDomainError):
    email: str

    def __init__(self, email: str):
        self.email = email


class UserNotExistsError(AuthDomainError):
    email: str

    def __init__(self, email: str):
        self.email = email


class PasswordNotMatchError(AuthDomainError):
    email: str

    def __init__(self, email: str):
        self.email = email
