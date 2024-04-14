# -*- coding: utf-8 -*-
# create by yihui 11:57 19/9/29
from bs4 import BeautifulSoup

from src.api.BaiscTask import BasicTask
from src.plugins.http import HttpTools
from src.plugins.http.HttpTools import ResultType
from src.plugins.logger.LoggerWrapper import SpiderLogger

DAY_THEME = ['c84c5306-f399-4c30-bfd4-ef96aeb40d90', 'd10ca665-5985-483b-8014-9d071d789603',
             'b20a2f77-547c-4bc9-93e4-54356de7cad8', '269cf914-a61a-4e1a-acc3-90eb1a88ee80',
             '59a201bb-835a-477a-a870-8b50eb480fef', '930aacbb-f3df-4198-8232-d4f07a4710e3',
             'cf6902d8-3ecf-4278-9124-697dcdf33d83', '036fcbc3-6897-4c0f-9e8e-7e33be1d926a',
             '39d0ff83-a9c6-481c-be0d-492fb3333ddf', '3d40c55f-0b39-42b6-97ad-b62a1ee2c14b',
             'c8331ec9-0b92-4784-a9ae-54aa995b03bd', 'c4474ce7-4e04-44d6-9173-b1939c0dd9f0',
             '7a029849-0782-4c67-ac2d-55f6895d84eb', '64053ccf-235b-4b50-a43f-38cecfbe0d3a',
             '261543e6-5202-41aa-a15f-f328b87a5c7b', 'e7696296-751b-4e33-a6d2-e632a26efa1e',
             'd28061be-dce6-4206-8740-316ad7982158', '8cc9e0df-3a8b-4e9b-83c3-a998eb60fa0f',
             '40835c16-d70e-40bb-bf94-10eb85158c71', '40e9c235-b38b-4c11-9a7b-b265839d0371',
             '0a4c726d-05f3-4aca-9516-4ea6a803b727', '38c218ea-f9fd-4974-b2d8-1a8e38cadb3e',
             '43fcba03-9a21-464c-9161-6950be5bf285', '75065786-267b-44a9-bf25-5ab117463049',
             '6b7ab216-3110-4565-9e50-7c7a15ca525b', 'cb12ceb2-8625-4e61-8d69-204ed7e61890',
             '7db71446-c52b-484c-ba0c-78a77c603b80', '8688512f-9383-4154-9b03-2e5373d704eb',
             '5b7c3780-19b1-4966-b543-7db259a8172b', '92952dec-77b3-448c-9325-30786e5154cd',
             'd3ed1796-bd02-4311-a20f-b58432836a75', '18617342-0c30-4924-b43f-ebc59c15879f',
             'b407c4db-5306-40d5-9023-046c9befc17f', '70d85946-d54e-477b-aa6e-735a7a98b11a',
             'dcdcf661-256a-4db2-9ab5-d84800a8b678', '0badab73-7107-4341-9883-7b7de98daa1b',
             '38dc116d-5445-4a8e-ae14-63485f0f9f13', 'e6d1d29c-e836-4429-b7c8-8e6435aa5e4c',
             '3c5c524a-2528-4257-856a-3de58f219901', '7fe8446e-9883-43c0-a32c-7c998bdbabcf',
             '1f01ed79-e3a5-4588-910d-ea59f9c21b87', 'cc684c6a-a1ae-4fc4-a8e1-e28f4e4dd687',
             '325fceb5-af42-42f5-94b0-80628884aac1', '2c7dbc72-7ee7-4a2d-b7c6-4259332ee26a',
             '1b42d97e-57ee-4a4f-a10d-301eec3c3b22', '26457a62-ef6f-48c2-a2b5-e0987a318994',
             'e8a4b48f-afc5-47fc-82fc-16edced1a99b', '8ce3e66a-6f10-4626-8f98-e1ca3024c5a2',
             'ac0d85d3-23c4-4f09-b39d-eba5c8ea3717', 'cce5bef5-c618-496c-a9db-10e4aa0f27c1',
             '37bf879f-1f4f-459e-91df-cf57299671f4', '57bb9b41-6f2a-4fa8-a404-73acd55db7aa',
             'cccd4ed5-7dd1-4e83-a17c-969b5f2f15a3', '0f934b0c-a79f-4588-a360-660c23abcc57',
             'b61457da-763c-4343-929b-15fcc6e5cabf', 'bafde848-a068-4633-a48c-39d7b8b8432c',
             '78e1d108-07bb-48a0-8f7f-ee8981b5811d', '3c1914d3-2e92-43bf-83c4-8d7ae49ecd94',
             '5a6ef0d7-5e49-4fd8-b2a9-1991e1f589d5', 'cf7e82e6-fdae-46cd-be28-915b3194a2f3',
             'ef6e401f-961f-411b-b6c3-be3dd6f9a07d', '481c11f8-efe3-48cd-9ca2-5e88e904769c',
             '9c2b9854-dbb7-40ad-bf43-8719c692d523', 'fb8adf17-2573-4112-93c5-ce7e5ca1ec22',
             '70935492-030b-472e-8164-527f50955c54', 'c529aa79-d36c-4559-a547-b49f555aef14',
             '068043f0-b3ec-4396-9fa5-9bc0ffa1b135', '83bfffa6-3c47-4c08-be95-f27298464326',
             '0f0ac3bf-0003-496a-8c00-0c28342d302b']

NIGHT_THEME = ['f3e3d901-3bf8-4ffe-afb6-0048b297694d', 'f43fa1f1-6662-4df5-b728-2add22ed5d27',
               '42edf0f3-e7c5-4998-8754-2a4e0d60f61c', 'f624a8e3-cc96-4c0c-95bb-43c8f7c257cc',
               'a7f14e49-40ae-4c84-8dbd-92190e0d898c', 'a2b29525-c177-42f5-9867-2406f436d072']

BG_IMGS = ['94e0d332-2669-4154-8b0e-01dfc678cbdc', 'fdd794d1-8b24-4d90-934e-a611a930f9dc',
           'b2fac362-ce7e-48d8-8823-dd182ee79067', 'bdbfa614-8498-4432-958d-5d86d4c6069f',
           '8d2a3e23-f123-4e83-b26f-c1a30aded57a']


class OwlThemeCrawler(BasicTask):

    async def async_init(self):
        SpiderLogger.info("初始化...")
        # self.mysql = await plugin_holder.load_mysql('kandian')
        # self.local = await plugin_holder.load_mysql('mysql')

    async def run(self):
        # await self.do_get_day_theme()
        await self.do_get_json()
        print("over")

    async def do_get_day_theme(self):
        response = []
        for id in DAY_THEME:
            url = f'https://flowus.cn/moshang/share/{id}'
            # page = await HttpTools.safe_requests(url, result_type=ResultType.PAGE)
            html = ''''''
            html = BeautifulSoup(html, 'html.parser')
            page = html.find('div', {'data-page-id': id})
            desc = page.find_all('div', {"class": 'relative cursor-text w-full my-px'})
            result = {
                'content': '',
                'imgs': [],
            }
            for sub in desc:
                result['content'] += '\n' + str(sub.text)

            links = page.find_all("div", {'class': 'relative'})
            for sub in links:
                l = sub.find('a')
                if l:
                    result['zip'] = l['href']
                    break

            imgs = page.find_all('div', {'class': 'relative cursor-text my-2.5 group self-center'})
            for img in imgs:
                img_tag = img.find('img')
                result['imgs'].append(str(img_tag['src']).strip())

            print(result)
            response.append(result)

    async def do_get_json(self):
        response = []
        for id in DAY_THEME:
            await self.do_fetch(id)
            # url = f'https://flowus.cn/api/docs/{id}'
            # res = await HttpTools.safe_requests(url, result_type=ResultType.JSON)
            # map = res['data']['blocks']
            #
            # result = {
            #     'txt': '',
            #     'imgs': [],
            #     'url': [],
            # }
            # for k, v in map.items():
            #     title = v['title']
            #     print(title, v['data'])
            #
            #     if str(title).endswith('.jpg'):
            #         continue
            #     result['txt'] += '\n' + title
            #
            # break
        print("----------")

    async def do_fetch(self, id):
        url = f"https://flowus.cn/api/docs/{id}"
        j_data = await HttpTools.safe_requests(url,
                                               cookies="AGL_USER_ID=0afe8332-6a63-48f1-808c-1b39958c56c7; bad_id29065810-5665-11ec-9024-1b3601704596=dc6d4f51-1a3a-11ed-b718-1b125cc200a9; locale=zh-cn",
                                               ResultType=ResultType.JSON)
        blocks = j_data['data']['blocks']
        title = []
        for block in blocks:
            title.append(block['title'])

        print(title)
