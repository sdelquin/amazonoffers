import requests
from bs4 import BeautifulSoup

import settings
from lib.utils import str2num


class Product:
    def __init__(self, url: str):
        response = requests.get(url, headers={'User-Agent': settings.USER_AGENT})
        soup = BeautifulSoup(response.content, 'html.parser')
        if span := soup.find('span', id='productTitle'):
            self.title = span.text.strip()
        if span := soup.find('span', class_='a-price-whole'):
            self.current_price = str2num(span.text)
        if span := soup.find('span', class_='savingsPercentage'):
            self.discount = str2num(span.text, int)
            if span := soup.find('span', class_='a-price a-text-price'):
                self.original_price = str2num(span.span.text)

    def has_discount(self) -> bool:
        return getattr(self, 'discount', None) is not None

    def __str__(self):
        buffer = []
        buffer.append(self.title)
        buffer.append('→')
        buffer.append(f'{self.current_price:.02f}€')
        if self.has_discount():
            buffer.append(f'(includes {self.discount}% discount)')
        return ' '.join(buffer)
