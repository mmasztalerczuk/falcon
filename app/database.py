import redis
from app import config


class RedisStorageEngine(object):
    def connection(self):
        pool = redis.ConnectionPool(host=config.REDIS_URL, port=config.REDIS_PORT)
        r = redis.Redis(connection_pool=pool)

        return r