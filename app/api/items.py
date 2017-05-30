import falcon
import uuid
import app.database as redis_db
import json

from app import logger
from app.api.update_db import add_new_cart, update_item
from app.errors import InvalidParameterError
from validator import validate_item_request

LOG = logger.get_logger()

class ReqItem(object):

    def __init__(self):
        db = redis_db.RedisStorageEngine()
        self.r = db.connection()


    @falcon.before(validate_item_request)
    def on_post(self, req, resp):

        data = req.context['data']

        if not 'cart_id' in data:
            # Creating new 'session'
            data['cart_id'] = str(uuid.uuid4())
            add_new_cart.delay(data)
            self.r.set(data['cart_id'], True)
            resp.set_cookie('cart_id', data['cart_id'])

        else:

            if not self.r.get(data['cart_id']):
                # There is no cert_id in redis db, so it means that user
                # is using wrong cart_id
                LOG.debug("Wrong cart_id")
                raise InvalidParameterError('Not existing cart_id')

        LOG.debug(data['external_id'])
        LOG.debug(self.r.get(data['external_id']))

        if self.r.get(data['external_id']):
            update_item.delay(data)
        else:
            raise InvalidParameterError('Not existing external_id')

        resp.body = json.dumps({'cart_id': data['cart_id']})
