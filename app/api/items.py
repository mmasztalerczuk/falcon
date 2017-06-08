import falcon
import uuid
import app.database as redis_db
import json

from app import logger
from app.api.update_db import add_new_cart, update_item
from app.errors import InvalidParameterError
from validator import validate_item_request

LOG = logger.get_logger()
CORES = 4


class ReqItem(object):

    def __init__(self):
        db = redis_db.RedisStorageEngine()
        self.r = db.connection()

    def get_queue_id(self, uuid):
        c = uuid[0]
        return str(ord(c) % CORES)

    @falcon.before(validate_item_request)
    def on_post(self, req, resp):

        data = req.context['data']

        if not self.r.get(data['external_id']):
            raise InvalidParameterError('Not existing external_id')

        if 'cart_id' not in data:
            # Creating new 'session'
            data['cart_id'] = str(uuid.uuid4())

            queue = 'q' + self.get_queue_id(data['cart_id'])
            add_new_cart.apply_async(args=[data], queue=queue)

            self.r.set(data['cart_id'], True)

        elif not self.r.get(data['cart_id']):
            # There is no cert_id in redis db, so it means that user
            # is using wrong cart_id
            LOG.debug("Wrong cart_id")
            raise InvalidParameterError('Not existing cart_id')

        LOG.debug(data['external_id'])
        LOG.debug(self.r.get(data['external_id']))

        queue = 'q' + self.get_queue_id(data['cart_id'])
        LOG.debug(queue)
        update_item.apply_async(args=[data], queue=queue)

        resp.body = json.dumps({'cart_id': data['cart_id']})
        resp.set_cookie('cart_id', data['cart_id'])
