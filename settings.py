from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

TARGET_URL = config('TARGET_URL', default='')
USER_AGENT = config(
    'USER_AGENT',
    default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
)
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
