from bs4 import BeautifulSoup
from logzero import logger

from lib.utils import http_get, str2num


class Product:
    def __init__(self, alias: str, url: str):
        logger.info(f'📦 Building product "{alias}"')
        self.alias = alias
        self.url = url
        response = http_get(url)
        if response.status_code != 200:
            raise BrokenPipeError(
                f'❌ Response with code {response.status_code}. No way to keep parsing!'
            )
        if 'CAPTCHA' in response.content.decode().upper():
            raise ValueError('❌ Captcha required. No way to keep parsing!')
        logger.debug('🍿 Extracting product features')
        soup = BeautifulSoup(response.content, 'html.parser')
        if span := soup.find('span', id='productTitle'):
            self.name = span.text.strip()
        if span := soup.find('span', class_='a-price-whole'):
            self.current_price = str2num(span.text)
        else:
            logger.error('🆘 Not able to locate current price of product')
        if span := soup.find('span', class_='savingsPercentage'):
            self.perc_discount = str2num(span.text, int)
            if span := soup.find('span', class_='a-price a-text-price'):
                self.original_price = str2num(span.span.text)
        else:
            self.perc_discount = 0
            self.original_price = self.current_price
        self.qty_discount = self.original_price - self.current_price

    @property
    def id(self) -> str:
        return self.url

    @property
    def template(self) -> str:
        if self.has_discount():
            return f"""**¡{self.name} en oferta!**

- {self.original_price:.02f}€ ↘️ **{self.current_price:.02f}€**
- **{self.perc_discount}%** ({self.qty_discount:.02f}€) de descuento.
- {self.url}
"""
        else:
            return f'{self.name} a precio normal'

    def has_discount(self) -> bool:
        return self.perc_discount > 0

    def __str__(self):
        return self.name
