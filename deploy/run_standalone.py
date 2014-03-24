#!/usr/bin/env python

# import logging
# import logging.config
#import os

#import config

from webfiles import app
from webfiles import views

#logging.config.dictConfig(config.logging_definition(config.LOGFILE['webapp']))


def main():
    app.run(debug=True, host='0.0.0.0', port=48001)


if __name__ == '__main__':
    main()
