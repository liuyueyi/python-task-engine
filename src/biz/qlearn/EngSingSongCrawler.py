from bs4 import BeautifulSoup

from src.api.BaiscTask import BasicTask
from src.env.EnvWrapper import env_wrapper
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger

URLS = [
    {
        'url': 'https://www.youtube.com/watch?v=IgXD4HsiKsU&list=PLii5rkhsE0LcUyqqaT86JlnkuRnjKXw1F&index=19&ab_channel=EnglishSingsing',
        'name': 'Educational Children Song'
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

        for seed in seeds:
            await self.down_url(seed['title'], seed['furl'])

    async def do_save_covers(self, seed):
        page = BeautifulSoup(contents, 'html.parser')
        item = page.find('div', {'id': 'items'})
        items = item.find_all('ytd-playlist-panel-video-renderer', {'id': "playlist-items"})
        ans = []
        for sub in items:
            title = sub.find('span', {'id': "video-title"})['title']
            title = str(title).strip()
            img = str(sub.find('img')['src']).strip()
            img = img[0: img.index('?')]
            print(f"{title} -> {img}")

    async def do_crawler(self, seed):
        # page = await HttpTools.safe_requests(seed['url'], proxy_enable=True, result_type=ResultType.PAGE)
        page = BeautifulSoup(contents, 'html.parser')
        item = page.find('div', {'id': 'items'})
        items = item.find_all('ytd-playlist-panel-video-renderer', {'id': "playlist-items"})
        ans = []
        for sub in items:
            title = sub.find('span', {'id': "video-title"})['title']
            img = str(sub.find('img')['src']).strip()
            img = img[0: img.index('?')]
            url = str(sub.find('a', {'id': 'wc-endpoint'})['href']).strip()
            full_url = f"https://www.youtubepp.com{url}"
            ans.append({
                'title': title,
                'url': url,
                'furl': full_url,
                'img': img,
            })

        ignore_titles = ['A Christmas Carol',
'A Dog of Flanders',
'Aladdin and the magic lamp',
'Beauty and the Beast',
'Cinderella ',
'Five Peas in a Pod',
'Goldilocks and the three bears',
'Hans in Luck',
'Hansel and Gretel',
'Heidi',
'Jack and the Beanstalk',
'Little Red Riding Hood',
'Princess and the Pea',
'Puss in Boots',
'Rudolf the RedNosed Reindeer',
'Rumpelstiltskin',
'Snow White and the Seven Dwarfs',
'The Ant and the Grasshopper',
'The Boy who Cried Wolf',
'The City Mouse and the Country Mouse',
'The Elves and the Shoemaker',
'The Fox and the Stork',
'The Frog Prince',
'The Gingerbread Man',
'The Goose that laid the Golden Eggs',
'The Happy Prince',
'The Hare and the Tortoise',
'The Little Match Girl',
'The Little Mermaid',
'The Little Prince',
'The Naked King',
'The North Wind and the Sun',
'The Pied Piper of Hamelin',
'The Prince and the Pauper',
'The Red Shoes',
'The Salt merchant and his Donkey',
'The Three Billy Goats Gruff',
'The Three Little Pigs',
'The Ugly Duckling',
'The Wild Swans',
'The Wizard of Oz',
'The sleeping beauty',
'TheBremenTownMusicians',
'Thumbelina',
'peter pan']
        for sub in ans:
            if sub['title'] in ignore_titles:
                continue

            print(f"{sub['title']} -- {sub['furl']}")
            seeds.append(sub)

    async def down_url(self, name, target):
        if target in [
            'https://www.youtubepp.com/watch?v=GD58KephpWE&list=PLii5rkhsE0Lc5f1FhF8l-QSDo7XO-0FkG&index=21&pp=iAQB']:
            return

        u1 = "https://www.y2mate.com/mates/en948/analyzeV2/ajax"
        params = {
            "k_query": target,
            'k_page': 'home',
            "hl": "en",
            "q_auto": 1
        }
        ans = await HttpTools.safe_requests(u1, method='post', proxy_enable=True, data=params, timeout=100,
                                            result_type=ResultType.JSON)
        # item = ans['links']['mp4']["137"] 1080p
        # item = ans['links']['mp4']["22"] # 720p
        item = None
        mp4_list = ans['links']['mp4']
        for k, sub in mp4_list.items():
            if sub['q'] == '720p':
                item = sub
                break
        if not item:
            item = ans['links']['mp4']["137"]


        durl = "https://www.y2mate.com/mates/convertV2/index"
        params = {
            "vid": ans['vid'],
            'k': item['k']
        }
        ans2 = await HttpTools.safe_requests(durl, method="post", proxy_enable=True, data=params, timeout=100,
                                             result_type=ResultType.JSON)
        print(f"{name} -> {ans2['dlink']}")
