import os

from src.api.BaiscTask import BasicTask
from src.plugins.logger.LoggerWrapper import SpiderLogger


class FileRemove(BasicTask):

    async def async_init(self):
        SpiderLogger.info("初始化...")
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        await self.crawler()

    async def crawler(self):
        f = 'C:\\Users\\bangz\\Videos\\英语学习-AZ\\cartoon story basic dialogue'
        ans = os.listdir(f)
        for item in ans:
            src = os.path.join(f, item)
            n_name = item.replace('y2mate.com - ', '').replace('_1080p', '').strip()
            out = os.path.join(f, n_name)
            os.rename(src, out)
            print(f'重命名: {src} -> {out}')
