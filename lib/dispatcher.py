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

    def dispatch(self):
        logger.info('🟩 Dispatching trackings')
        for cfg_block in self.config:
            user_config = cfg_block['user']
            user = User(user_config['name'], user_config['email'])
            products_config = cfg_block['products']
            for product_config in products_config:
                try:
                    product = Product(product_config['alias'], product_config['url'])
                except Exception as err:
                    logger.error(err)
                    continue
                min_discount = product_config.get('min_discount', 0)
                tracking = Tracking(user, product)
                if product.has_discount():
                    logger.debug(f'🔥 Product "{product.alias}" has discount!')
                    if product.perc_discount >= min_discount:
                        if min_discount > 0:
                            logger.debug(
                                f'✨ Product "{product.alias}" is over the required discount of {min_discount}%'
                            )
                        if notified_price := tracking.get_notified_price():
                            if product.current_price < notified_price:
                                logger.debug(
                                    'Current price is lower than notified price (in the past)'
                                )
                                tracking.update_delivery()
                                tracking.notify()
                            else:
                                logger.debug(
                                    f'👎 Notification discarded. It was already notified to "{user}"'
                                )
                        else:
                            tracking.update_delivery()
                            tracking.notify()
                    else:
                        logger.debug(
                            f'😕 Product "{product.alias}" has not reach the required discount of {min_discount}%'
                        )
                else:
                    logger.debug(f'⚪ Product "{product.alias}" has normal price')
                    if tracking.get_notified_price():
                        logger.debug('Delivery will be removed since product has no yet discount')
                        tracking.remove_delivery()

    def clean_orphan_deliveries(self) -> None:
        logger.info('🧽 Cleaning orphan deliveries')
        for delivery in Tracking.deliveries:
            found = False
            for cfg_block in self.config:
                user_config = cfg_block['user']
                products_config = cfg_block['products']
                for product_config in products_config:
                    tracking_id = f'{user_config['email']}:{product_config['url']}'
                    if delivery == tracking_id:
                        found = True
                        break
                if found:
                    break
            if not found:
                logger.info(f'❌ Delivery "{delivery}" is orphan. Deleting')
                del Tracking.deliveries[delivery]
