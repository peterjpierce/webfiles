import logging
import logging.config

import settings.config as cfg
logging.config.dictConfig(cfg.LOGGING_CONFIG)

from webfiles import app as application
