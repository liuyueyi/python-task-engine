# -*- coding: utf-8 -*-
# create by yihui 10:12 19/10/9
import asyncio

from src.plugins.logger.LoggerWrapper import SpiderLogger
from src.plugins.mysql.MysqlWrapper import mysql_wrapper, MysqlWrapper
from src.plugins.redis.RedisWrapper import RedisWrapper, redis_wrapper

MYSQL_KEY = "mysql"
DEFAULT_MYSQL = "mysql"

REDIS_KEY = "redis"
DEFAULT_REDIS_CONF_KEY = "redis"


class PluginHolder:
    def __init__(self):
        self._resource_holder = {}
        pass

    async def load_mysql(self, key=DEFAULT_MYSQL):
        if MYSQL_KEY not in self._resource_holder:
            self._resource_holder[MYSQL_KEY] = {}

        if key not in self._resource_holder[MYSQL_KEY]:
            tmp = mysql_wrapper if key == DEFAULT_MYSQL else MysqlWrapper()
            await tmp.connect(key)
            self._resource_holder[MYSQL_KEY][key] = tmp

        await asyncio.sleep(0)
        return self._resource_holder[MYSQL_KEY][key]

    def load_redis(self, key="redis"):
        if REDIS_KEY not in self._resource_holder:
            self._resource_holder[REDIS_KEY] = {}

        if key not in self._resource_holder[REDIS_KEY]:
            tmp = redis_wrapper if key == DEFAULT_REDIS_CONF_KEY else RedisWrapper()
            tmp.connect(key)
            self._resource_holder[REDIS_KEY][key] = tmp

        return self._resource_holder[REDIS_KEY][key]

    async def release(self):
        # 需要主动回收资源的有 mysql
        if MYSQL_KEY in self._resource_holder:
            for mysql in self._resource_holder[MYSQL_KEY].values():
                await mysql.close()

        if REDIS_KEY in self._resource_holder:
            for redis in self._resource_holder[REDIS_KEY].values():
                redis.close()

        await asyncio.sleep(0)
        SpiderLogger.debug("finish release all resources!")


plugin_holder = PluginHolder()
