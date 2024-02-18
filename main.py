from lib.dispatcher import Dispatcher
from lib.utils import init_logger

logger = init_logger()

d = Dispatcher()
d.dispatch()
