import shelve

import settings
from lib.products import Product
from lib.users import User


class Tracking:
    deliveries = shelve.open(settings.STORAGE_PATH)

    def __init__(self, user: User, product: Product):
        self.user = user
        self.product = product

    @property
    def tagline(self) -> str:
        return f'{self.user.email}:{self.product.id}'

    def was_notified(self):
        return self.tagline in self.deliveries
