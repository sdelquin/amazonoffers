import yaml

import settings
from lib.products import Product
from lib.trackings import Tracking
from lib.users import User


class Dispatcher:
    def __init__(self, config_path=settings.CONFIG_PATH):
        self.config = yaml.safe_load(config_path.read_text())

    def dispatch(self):
        for cfg_block in self.config:
            user_config = cfg_block['user']
            user = User(user_config['name'], user_config['email'])
            products_config = cfg_block['products']
            for product_config in products_config:
                product = Product(product_config['alias'], product_config['url'])
                tracking = Tracking(user, product)
                if product.has_discount():
                    if notified_price := tracking.get_notified_price():
                        if product.current_price < notified_price:
                            tracking.update_delivery()
                            tracking.notify()
                    else:
                        tracking.update_delivery()
                        tracking.notify()
                elif tracking.get_notified_price():
                    tracking.remove_delivery()
