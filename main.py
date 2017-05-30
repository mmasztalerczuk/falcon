# -*- coding: utf-8 -*-

import falcon
import celery

from app.api import items
from app import logger
from app.middleware import JSONTranslator
from app.errors import AppError

LOG = logger.get_logger()

class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        self.add_route('/item', items.ReqItem())
        self.add_error_handler(AppError, AppError.handle)

middleware = [JSONTranslator()]
app = celery.Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
main = App(middleware=middleware)


