# -*- coding: utf-8 -*-
# create by yihui 11:57 19/9/29
import json

from src.api.BaiscTask import BasicTask
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger


class UisdcCrawler(BasicTask):
    """
    https://hao.uisdc.com/ 设计导航数据
    """

    async def async_init(self):
        SpiderLogger.info("初始化...")

    async def run(self):
        page = await HttpTools.safe_requests('https://hao.uisdc.com/', result_type=ResultType.PAGE)
        tabs = page.find_all("div", {'class': 'part'})
        result = []
        for tab in tabs:
            ans = await self.get_sub_items(tab)
            result.extend(ans)

        res = json.dumps(result)
        SpiderLogger.info(f"{res}")

    async def get_sub_items(self, page):
        link_tag = page.find('h2', {'class': 'has_link'})
        result = []
        if link_tag:
            # 存在时，到子页面爬取
            new_url = link_tag.find('a')['href']
            new_page = await HttpTools.safe_requests(new_url, result_type=ResultType.PAGE)
            tabs = new_page.find_all('div', {'class': 'part'})
            for tab in tabs:
                res = await self.get_sub_items(tab)
                result.extend(res)
        else:
            items = page.find_all('div', {'class': 'item'})
            sub_list = []
            for item in items:
                icon = item.find('img')['src']
                name = str(item.find('h3').text).strip()
                desc = str(item.find('p').text).strip()
                path = str(item.find('a')['href']).strip()
                sub_list.append({
                    'name': name,
                    'desc': desc,
                    'icon': icon,
                    'search_keys': '',
                    'path': path,
                    'hot': 100,
                })

            tab = {
                'title': str(page['data-title']).strip(),
                'icon': '',
                'tab': str(page['id']).strip(),
                'list': sub_list
            }
            result.append(tab)

        return result
