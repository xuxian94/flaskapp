# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from flaskapp.app import create_app
from flaskapp.settings import DevConfig, ProdConfig

import sys

reload(sys)

sys.setdefaultencoding("utf-8")

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
