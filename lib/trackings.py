import shelve

from logzero import logger
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

    def __init__(self, user: User, product: Product, min_discount=0):
        logger.info(f'🔎 Building tracking "{user.name}:{product.alias}"')
        self.user = user
        self.product = product
        self.min_discount = min_discount

    @property
    def id(self) -> str:
        return f'{self.user.id}:{self.product.id}'

    def get_notified_price(self) -> float | None:
        return self.deliveries.get(self.id, None)

    def remove_delivery(self) -> None:
        logger.debug('Removing delivery')
        del self.deliveries[self.id]

    def update_delivery(self) -> None:
        logger.debug('Updating delivery')
        self.deliveries[self.id] = self.product.current_price

    def notify(self) -> None:
        logger.debug(f'📮 Notifying offer "{self.product.alias}" to "{self.user.name}"')
        self.sg.send(
            to=self.user.email,
            subject=self.product.name,
            msg=self.product.template,
            as_markdown=True,
        )
