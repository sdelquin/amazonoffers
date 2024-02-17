import re

import requests
from bs4 import BeautifulSoup

import settings

response = requests.get(settings.TARGET_URL, headers={'User-Agent': settings.USER_AGENT})
soup = BeautifulSoup(response.content, 'html.parser')
if offer := soup.find('span', class_='savingsPercentage'):
    if discount := re.search(r'\d+', offer.text):
        print(discount[0])
