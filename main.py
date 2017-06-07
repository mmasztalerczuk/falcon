# -*- coding: utf-8 -*-

import falcon

from app.api import items
from app import logger
from app.middleware.json_parser import JSONTranslator
from app.errors import AppError

LOG = logger.get_logger()


class App(falcon.API):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        self.add_route('/item', items.ReqItem())
        self.add_error_handler(AppError, AppError.handle)


middleware = [JSONTranslator()]

main = App(middleware=middleware)
