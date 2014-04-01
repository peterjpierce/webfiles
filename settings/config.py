import os

DEBUG = True
FILES_ROOT = '/home/peter/dev/var/file_depot'
TIMEOUT_MINUTES = 30

SECRET_KEY = 'thisiscobblegobbled_c12e955bb726'
CSRF_ENABLED = True

BASEDIR = os.path.abspath('%s/..' % os.path.dirname(__file__))

LOGFILE = '%s/var/log/webfile.log' % BASEDIR
LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '%(asctime)s [%(process)5d] (%(name)s) %(levelname)s - %(message)s',
                },
            },
        'handlers': {
            'logfile': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': LOGFILE,
                'when': 'W6',
                'backupCount': 26,
                'level': 'DEBUG' if DEBUG else 'INFO',
                'formatter': 'basic',
                },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG' if DEBUG else 'INFO',
                'formatter': 'basic',
                'stream': 'ext://sys.stdout',
                },
            },
        'root': {
            # most verbose here, let handlers be the filters
            'level': 'DEBUG',
            'handlers': ['logfile', 'console'] if DEBUG else ['logfile',],
            },
        }
