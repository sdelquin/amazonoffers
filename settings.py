from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent

TARGET_URL = config('TARGET_URL', default='')
USER_AGENT = config(
    'USER_AGENT',
    default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
)
CONFIG_PATH = config('CONFIG_PATH', default=PROJECT_DIR / 'config.yaml', cast=Path)
STORAGE_PATH = config('STORAGE_PATH', default='deliveries.dbm')
