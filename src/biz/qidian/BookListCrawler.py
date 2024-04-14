# -*- coding: utf-8 -*-
# create by yihui 11:57 19/9/29

from src.api.BaiscTask import BasicTask
from src.env.EnvWrapper import env_wrapper
from src.plugins.PluginHolder import plugin_holder
from src.plugins.logger.LoggerWrapper import SpiderLogger


class DemoCrawler(BasicTask):

    async def async_init(self):
        SpiderLogger.info("初始化...")
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        SpiderLogger.info(f"输出一个日志!!!! {env_wrapper.is_pro()}")
        SpiderLogger.info(f"另外一个日志 ", name="other")
