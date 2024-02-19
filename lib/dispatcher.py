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
                tracking = Tracking(user, product, product_config.get('min_discount', 0))
                tracking.dispatch()

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
