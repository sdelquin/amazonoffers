import shelve

from sendgrify import SendGrid

import settings
from lib.products import Product
from lib.users import User


class Tracking:
    deliveries = shelve.open(settings.STORAGE_PATH)
    sg = SendGrid(
        settings.SENDGRID_APIKEY,
        settings.SENDGRID_FROM_ADDR,
        settings.SENDGRID_FROM_NAME,
    )

    def __init__(self, user: User, product: Product):
        self.user = user
        self.product = product

    @property
    def id(self) -> str:
        return f'{self.user.id}:{self.product.id}'

    def get_notified_price(self) -> float | None:
        return self.deliveries.get(self.id, None)

    def remove_delivery(self) -> None:
        del self.deliveries[self.id]

    def update_delivery(self) -> None:
        self.deliveries[self.id] = self.product.current_price

    def notify(self) -> None:
        self.sg.send(
            to=self.user.email,
            subject=self.product.name,
            msg=self.product.template,
            as_markdown=True,
        )
