# -*- coding: utf-8 -*-
# create by yihui 14:12 18/12/20
import asyncio
import aiomysql

from src.env.EnvWrapper import env_wrapper
from src.plugins.logger.LoggerWrapper import SpiderLogger


class MysqlWrapper:
    def __init__(self):
        self._pool = None

    async def connect(self, key="mysql"):
        assert env_wrapper.get_conf() is not None, "配置器未初始化"
        mysql_config = env_wrapper.get_conf(key)
        try:
            self._pool = await aiomysql.create_pool(
                host=mysql_config['host'],
                port=mysql_config['port'],
                user=mysql_config['username'],
                password=mysql_config['password'],
                db=mysql_config['db_name'],
                use_unicode=True,
                charset="utf8mb4")
            SpiderLogger.debug("mysql连接上数据库{}".format(mysql_config['host']))
            return True
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            SpiderLogger.error(f"mysql : {mysql_config}")
            SpiderLogger.error(f"mysql数据库连接失败：{ex!r}")
            return False

    async def close(self):
        if self._pool is not None:
            SpiderLogger.debug("mysql将断开数据库连接！")
            self._pool.close()
            await self._pool.wait_closed()

    async def execute_one(self, sql):
        conn = await self._pool.acquire()
        try:
            cur = await conn.cursor()
            await cur.execute(sql)
            await conn.commit()
            # 如果执行插入，则返回最新的id；如果是更新，返回的0
            return cur.lastrowid
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            SpiderLogger.error("执行语句{}时出错:{}，如有需要请检查结果!".format(sql, ex))
        finally:
            self._pool.release(conn)

    async def execute_many(self, stmt, data):
        conn = await self._pool.acquire()
        try:
            cur = await conn.cursor()
            await cur.executemany(stmt, data)
            await conn.commit()
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            SpiderLogger.error("执行语句时出错:{}，如有需要请检查结果!".format(ex))
        finally:
            self._pool.release(conn)

    async def fetch_one(self, sql):
        one = None
        conn = await self._pool.acquire()
        try:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(sql)
            one = await cur.fetchone()
            await conn.commit()
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            SpiderLogger.error("执行语句{}时出错:{}，如有需要请检查结果!".format(sql, ex))
        finally:
            self._pool.release(conn)
        return one

    async def fetch_all(self, sql):
        all_ = None
        conn = await self._pool.acquire()
        try:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(sql)
            all_ = await cur.fetchall()
            await conn.commit()
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            SpiderLogger.error("执行语句{}时出错:{}，如有需要请检查结果!".format(sql, ex))
        finally:
            self._pool.release(conn)
        return all_


mysql_wrapper = MysqlWrapper()
connect = mysql_wrapper.connect
close = mysql_wrapper.close
execute_one = mysql_wrapper.execute_one
execute_many = mysql_wrapper.execute_many
fetch_one = mysql_wrapper.fetch_one
fetch_all = mysql_wrapper.fetch_all
