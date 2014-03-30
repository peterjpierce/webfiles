#!/usr/bin/env python

import logging
import logging.config

import settings.config as cfg
from webfiles import app

logging.config.dictConfig(cfg.LOGGING_CONFIG)


def main():
    app.run(debug=True, host='0.0.0.0', port=48001)


if __name__ == '__main__':
    main()
