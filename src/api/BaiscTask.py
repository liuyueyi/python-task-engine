# -*- coding: utf-8 -*-
# create by yihui 10:58 19/9/29
import asyncio

from src.plugins.logger.LoggerWrapper import SpiderLogger


class BasicTask:
    def __init__(self):
        pass

    async def async_init(self):
        pass

    async def _run_before(self):
        """
        任务执行前被回调
        :return:
        """
        await asyncio.sleep(0)

    async def _run_after(self, data):
        """
        任务执行后被回调
        :param data:
        :return:
        """
        await asyncio.sleep(0)

    async def call(self):
        try:
            await self._run_before()
            data = await self.run()
            await self._run_after(data)
            return data
        except Exception as e:
            SpiderLogger.exception("some exception!", "core")
            return 'Exception!'

    async def run(self):
        """
        具体的业务执行
        :return:
        """
        raise NotImplementedError()
