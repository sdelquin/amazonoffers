from pathlib import Path

from fake_useragent import UserAgent
from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_PATH = config('CONFIG_PATH', default=PROJECT_DIR / 'config.yaml', cast=Path)
STORAGE_PATH = config('STORAGE_PATH', default='deliveries.dbm')

SENDGRID_APIKEY = config('SENDGRID_APIKEY', default='your-sendgrid-api-key-here')
SENDGRID_FROM_ADDR = config('SENDGRID_FROM_ADDR', default='from@example.com')
SENDGRID_FROM_NAME = config('SENDGRID_FROM_NAME', default='From Example')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

PROXY_URI = config('PROXY_URI', default='')
PROXIES = dict(http=PROXY_URI, https=PROXY_URI) if PROXY_URI else {}
DELAY_BETWEEN_REQUESTS = config('DELAY_BETWEEN_REQUESTS', default='0', cast=int)  # seconds


USER_AGENT = config('USER_AGENT', default=UserAgent().random)
