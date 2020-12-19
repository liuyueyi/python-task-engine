# -*- coding: utf-8 -*-
# create by yihui 10:46 19/1/4
import redis as redis

from src.env.EnvWrapper import env_wrapper


class RedisWrapper:
    def __init__(self):
        self._pool = None

    def connect(self, key="redis"):
        assert env_wrapper.get_conf() is not None, "配置器未初始化"
        redis_conf = env_wrapper.get_conf(key)
        self._pool = redis.ConnectionPool(host=redis_conf['host'], port=redis_conf['port'],
                                          password=redis_conf['password'])

    def close(self):
        """
        释放连接
        :return:
        """
        self._pool.disconnect()

    def get(self, key):
        r = redis.Redis(connection_pool=self._pool)
        return r.get(key)

    def set(self, key, value, ex=None):
        r = redis.Redis(connection_pool=self._pool)
        return r.set(key, str(value), ex=ex)

    def lpush(self, key, value):
        r = redis.Redis(connection_pool=self._pool)
        return r.lpush(key, str(value))

    def lrange(self, key, start, end):
        r = redis.Redis(connection_pool=self._pool)
        return r.lrange(key, start, end)

    def hget(self, key, field):
        r = redis.Redis(connection_pool=self._pool)
        return r.hget(key, field)

    def hset(self, key, field, value):
        r = redis.Redis(connection_pool=self._pool)
        return r.hset(key, field, value)

    def hmget(self, key, fields):
        r = redis.Redis(connection_pool=self._pool)
        return r.hmget(key, fields)


redis_wrapper = RedisWrapper()
