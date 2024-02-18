class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property
    def id(self) -> str:
        return self.email
