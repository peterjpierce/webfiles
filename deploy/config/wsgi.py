#import logging
#import logging.config

#import config
#logging.config.dictConfig(config.logging_definition(config.LOGFILE['webapp']))

from webfiles import app as application
