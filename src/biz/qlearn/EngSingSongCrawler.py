from bs4 import BeautifulSoup

from src.api.BaiscTask import BasicTask
from src.env.EnvWrapper import env_wrapper
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger

URLS = [
    {
        'url': 'https://www.youtube.com/watch?v=NylcpKgVNII&list=PLii5rkhsE0LcDfBlM522YW0h9fE2yLH2f&index=3&ab_channel=EnglishSingsing',
        'name': 'alphabet song'
    }
]

seeds = []

contents = ""


class EngSingSongCrawler(BasicTask):

    async def async_init(self):
        SpiderLogger.info("初始化...")
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        await self.crawler()

    async def crawler(self):
        down = 1
        if down == 1:
            for url in URLS:
                await self.do_crawler(url)
        else:
            for seed in seeds:
                await self.down_url(seed)

    async def do_crawler(self, seed):
        # page = await HttpTools.safe_requests(seed['url'], proxy_enable=True, result_type=ResultType.PAGE)
        page = BeautifulSoup(contents, 'html.parser')
        item = page.find('div', {'id': 'items'})
        items = item.find_all('ytd-playlist-panel-video-renderer', {'id': "playlist-items"})
        ans = []
        for sub in items:
            title = sub.find('span', {'id': "video-title"})['title']
            url = str(sub.find('a', {'id': 'wc-endpoint'})['href']).strip()
            full_url = f"https://www.youtubepp.com{url}"
            ans.append({
                'title': title,
                'url': url,
                'furl': full_url
            })

        for sub in ans:
            print(f"{sub['title']} -- {sub['furl']}")

        print(ans)

    async def down_url(self, target):
        u1 = "https://www.y2mate.com/mates/analyzeV2/ajax"
        params = {
            "k_query": target,
            "hl": "en",
            "q_auto": 1
        }
        ans = await HttpTools.safe_requests(u1, method='post', proxy_enable=True, data=params,
                                            result_type=ResultType.JSON)
        item = ans['links']['mp4']["137"]

        durl = "https://www.y2mate.com/mates/convertV2/index"
        params = {
            "vid": ans['vid'],
            'k': item['k']
        }
        ans2 = await HttpTools.safe_requests(durl, method="post", proxy_enable=True, data=params,
                                             result_type=ResultType.JSON)
        print(f"{target} -> {ans2['dlink']}")
