# -*- coding: utf-8 -*-
# create by yihui 11:57 19/9/29
import json

from src.api.BaiscTask import BasicTask
from src.env.EnvWrapper import env_wrapper
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger


class MycmsCrawler(BasicTask):
    """
    https://nav.mycms.net.cn/ 导航数据爬取
    """

    async def async_init(self):
        SpiderLogger.info("初始化...")
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        SpiderLogger.info(f"输出一个日志!!!! {env_wrapper.is_pro()}")
        SpiderLogger.info(f"另外一个日志 ", name="other")
        page = await HttpTools.safe_requests('https://nav.mycms.net.cn/', result_type=ResultType.PAGE)
        tabs = self.get_tabs(page)
        result = []
        for tab in tabs:
            items = self.get_items(tab, page)
            result.append({
                'title': tab['name'],
                'icon': '',
                'tab': '',
                'list': items
            })

        res = json.dumps(result)
        SpiderLogger.info(f"{res}")

    def get_tabs(self, page):
        nav_bar = page.find('dl', {'id': 'hSiteNav'})
        navs = nav_bar.find_all('dd')
        result = []
        for nav in navs:
            result.append({
                'name': str(nav.text).strip(),
                'id': str(nav['data-id']).strip(),
            })
        return result

    def get_items(self, tab, page):
        items = page.find('ul', {'id': f'ul-{tab["id"]}'}).find_all('li', {'class': 'item'})
        result = []
        for item in items:
            img = str(item.find('img')['src']).strip()
            text = str(item.find('span', {'class': 'text'}).text).strip()
            href = str(item.find('a')['href']).strip()
            result.append({
                'name': text,
                'icon': img,
                'search_keys': '',
                'path': href,
                'hot': 100,
            })

        return result
