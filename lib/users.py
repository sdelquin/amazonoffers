from logzero import logger


class User:
    def __init__(self, name: str, email: str):
        logger.info(f'👤 Building user "{name}"')
        self.name = name
        self.email = email

    @property
    def id(self) -> str:
        return self.email

    def __str__(self):
        return self.name
