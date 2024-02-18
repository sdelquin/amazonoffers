import yaml

import settings
from lib.products import Product

config = yaml.safe_load(settings.CONFIG_PATH.read_text())
for url in config:
    p = Product(url)
    print(p)
