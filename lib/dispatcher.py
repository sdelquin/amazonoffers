import yaml
from logzero import logger

import settings
from lib.products import Product
from lib.trackings import Tracking
from lib.users import User


class Dispatcher:
    def __init__(self, config_path=settings.CONFIG_PATH):
        logger.info(f'🔄 Loading configuration from {config_path}')
        self.config = yaml.safe_load(config_path.read_text())
        self.trackings = []
        for cfg_block in self.config:
            user_config = cfg_block['user']
            user = User(user_config['name'], user_config['email'])
            products_config = cfg_block['products']
            for product_config in products_config:
                try:
                    product = Product(product_config['alias'], product_config['url'])
                except Exception as err:
                    logger.error(err)
                else:
                    self.trackings.append(Tracking(user, product))

    def dispatch(self):
        logger.info('🟩 Dispatching trackings')
        for tracking in self.trackings:
            if tracking.product.has_discount():
                logger.debug(f'🔥 Product "{tracking.product.alias}" has discount!')
                if notified_price := tracking.get_notified_price():
                    if tracking.product.current_price < notified_price:
                        logger.debug('Current price is lower than notified price (in the past)')
                        tracking.update_delivery()
                        tracking.notify()
                    else:
                        logger.debug(
                            f'👎 Notification discarded. It was already notified to "{tracking.user}"'
                        )
                else:
                    tracking.update_delivery()
                    tracking.notify()
            else:
                logger.debug(f'😐 Product "{tracking.product.alias}" has normal price')
                if tracking.get_notified_price():
                    logger.debug('Delivery will be removed since product has no yet discount')
                    tracking.remove_delivery()

    def clean_orphan_deliveries(self) -> None:
        logger.info('🧽 Cleaning orphan deliveries')
        for delivery in Tracking.deliveries:
            for tracking in self.trackings:
                if delivery == tracking.id:
                    break
            else:
                logger.info(f'✗ Delivery "{delivery}" is orphan. Deleting')
                del Tracking.deliveries[delivery]
