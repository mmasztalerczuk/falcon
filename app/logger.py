# -*- coding: utf-8 -*-
import logging

from logging.handlers import RotatingFileHandler
from app import config


logging.basicConfig(level=config.LOG_LEVEL)
LOG = logging.getLogger('API')
LOG.propagate = False

INFO_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
DEBUG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] ' \
               '%(message)s [in %(pathname)s:%(lineno)d]'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %z'
file_handler = RotatingFileHandler('log/app.log', 'a', 1 * 1024 * 1024, 10)
formatter = logging.Formatter(INFO_FORMAT, TIMESTAMP_FORMAT)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)


def get_logger():
    return LOG
