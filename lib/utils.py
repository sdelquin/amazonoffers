import re
import time

import logzero
import requests
from logzero import logger

import settings


def str2num(text: str, cast=float) -> float | int:
    if m := re.search(r'(\d+)(?=[.,](\d+))?[€$]?', text):
        int_part, dec_part = m.groups()
        num = float(f'{int_part}.{dec_part or 0}')
        return cast(num)
    raise ValueError(f'Cannot parse "{text}" into number')


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def http_get(
    url: str,
    delay: int = settings.DELAY_BETWEEN_REQUESTS,
    user_agent: str = settings.USER_AGENT,
    proxies: str = settings.PROXIES,
) -> requests.Response:
    logger.debug(f'🌐 Request to {url}')
    if delay > 0:
        logger.debug(f'😴 Applying delay of {delay}s.')
        time.sleep(delay)
    if proxies:
        logger.debug(f'🚪 Using proxies {proxies}')
    logger.debug(f'🔘 User agent: {user_agent}')
    return requests.get(url, headers={'User-Agent': user_agent}, proxies=settings.PROXIES)
