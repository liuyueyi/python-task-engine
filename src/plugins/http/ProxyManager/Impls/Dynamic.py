import json
import time

import requests

from src.plugins.http.ProxyManager.AbstractProxy import AbstractProxy


class Dynamic(AbstractProxy):
    REQ_URL = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=" \
              "dd5ae8c1448949ebb36412bfc9c7d5f2&orderno=YZ20186230021dCAg1S&returnType=2&count=20"
    # 最小拉取间隔：5秒
    MIN_PULL_INTERVAL = 5

    def _pull_ips(self):
        """
        获取代理ip
        :return:
        """
        while True:
            response = json.loads(requests.get(Dynamic.REQ_URL).text)
            if response.get("ERRORCODE") != '0':
                print("RE_PULL")
                print(response.get("ERRORCODE"))
                time.sleep(Dynamic.MIN_PULL_INTERVAL)
                continue
            result = response.get("RESULT")
            for data in result:
                if isinstance(data, dict):
                    self.ip_pool.append("{}:{}".format(data.get("ip"), data.get("port")))
                    break

    def pop_proxy(self):
        """
        返回一个proxy
        :return:
        """
        if len(self.ip_pool) < 10:
            self.pull_ips()
        item = len(self.good_ip)
        if item > 10:
            proxy = self.good_ip.pop()
        else:
            proxy = self.ip_pool.pop()

        self.start_time = time.time()
        return "http://{}".format(proxy)

    def _proxy_success(self, proxy):
        """
        获取成功
        :return:
        """
        ip = proxy.replace("http://", "")
        self.good_ip.insert(0, ip)

    def _proxy_missing(self):

        pass

    def proxy_done(self, proxy, success=True):
        pass

    def _update_ip_pool(self, proxy):
        """
        更新ip池
        :return:
        """
        self.end_time = time.time()
        print(self.time_consuming)
