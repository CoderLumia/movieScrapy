import redis
from movieScrapy.settings import REDIS_CONFIG


class RedisUtil:
    __POOL = redis.ConnectionPool(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], max_connections=10,
                                  db=REDIS_CONFIG['db'])

    @staticmethod
    def get_and_increment(key):
        con = redis.Redis(connection_pool=RedisUtil.__POOL, decode_responses=True)
        return con.incr(key, amount=1)

    @staticmethod
    def push(key, values):
        con = redis.Redis(connection_pool=RedisUtil.__POOL, decode_responses=True)
        con.lpush(key, values)

    @staticmethod
    def pop(key):
        con = redis.Redis(connection_pool=RedisUtil.__POOL, decode_responses=True)
        return con.rpop(key)
