# -*- coding: utf-8 -*-
# create by yihui 11:57 19/9/29
import json

from src.api.BaiscTask import BasicTask
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger

urls = [
    # {'url': 'https://www.zdzn.net/page/total.html', 'name': '综合', 'tab': 'total'},
    {'url': 'https://www.zdzn.net/page/web.html', 'name': '前端', 'tab': 'web'},
    {'url': 'https://www.zdzn.net/page/android.html', 'name': 'Android', 'tab': 'android'},
    {'url': 'https://www.zdzn.net/page/backend.html', 'name': '后端', 'tab': 'server'},
    {'url': 'https://www.zdzn.net/page/php.html', 'name': 'php', 'tab': 'php'},
    {'url': 'https://www.zdzn.net/page/node.html', 'name': 'node.js', 'tab': 'node'},
]


class ZdznCrawler(BasicTask):
    """
    https://https://www.zdzn.net/ 导航数据爬取
    """

    async def async_init(self):
        pass
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        result = []
        title = None
        for item in urls:
            url = item['url']
            page = await HttpTools.safe_requests(url, result_type=ResultType.PAGE)
            sub_lives = page.find_all('div', {'class': 'classify-descRow'})
            nav = {}
            for sub in sub_lives:
                tmp = self.parse_sub_nav(sub)
                if tmp['nav']:
                    title = tmp
                else:
                    if not title:
                        title = {'title': ''}
                    if title['title'] in nav.keys():
                        tools = nav[title['title']]
                    else:
                        tools = []

                    tools.extend(tmp['tools'])
                    nav[title['title']] = tools

            sub_nav = []
            for k, v in nav.items():
                sub_nav.append({
                    'title': k,
                    'tab': k,
                    'icon': '',
                    'list': v,
                })
            result.append({
                'title': item['name'],
                'tab': item['tab'],
                'icon': '',
                'from': url,
                'sub_nav': sub_nav
            })

        res = json.dumps(result)
        print(res)
        SpiderLogger.info(f"{res}")

    def parse_sub_nav(self, sub):
        title = sub.find('div', {'class': 'classify-titleItem'})
        if title:
            nav_title = title.find('span').text
            return {
                "title": nav_title,
                "nav": True,
            }
        else:
            items = sub.find_all('div', {'class': 'classify-descItem'})
            tools = []
            for item in items:
                path = item.find('a')['href']
                icon = str(item.find('img')['src']).replace("../", 'https://www.zdzn.net/').strip()
                name = item.find('a').find('span').text
                desc = item.find('span', {'class': 'item-desc'}).text
                tools.append({
                    'name': name,
                    'desc': desc,
                    'icon': icon,
                    'search_keys': '',
                    'path': path,
                    'hot': 100,
                })
            return {
                "tools": tools,
                "nav": False
            }
