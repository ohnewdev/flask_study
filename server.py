from flask.helpers import get_debug_flag

from diary import create_app
from diary.settings import DevConfig, ProdConfig

#CONFIG = DevConfig if get_debug_flag() else ProdConfig
CONFIG = DevConfig
app = create_app(CONFIG)
