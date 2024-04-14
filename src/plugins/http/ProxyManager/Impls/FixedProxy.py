# 固定IP方案

import time
import asyncio

from src.plugins.http.ProxyManager.AbstractProxy import AbstractProxy


class FixedProxy(AbstractProxy):
    # 用一个proxy被拉取的最小间隔时间
    MIN_TIME_DIFFERENCE = 0.5

    def __init__(self):
        self._ip_pool = [
            {"ip": "http://127.0.0.1:10809", "time": 0},
           ]

    def _pull_ips(self):
        """
        添加固定ip
        :return:
        """
        return self._ip_pool

    @asyncio.coroutine
    def pop_proxy(self):
        """
        弹出一个格式规整的proxy
        :return:
        """
        while True:
            if len(self._ip_pool) >= 1:
                proxy = min(self._ip_pool, key=lambda x: x.get("time"))
                if time.time() < proxy.get("time") + FixedProxy.MIN_TIME_DIFFERENCE:
                    yield from asyncio.sleep(0.5)
                if proxy in self._ip_pool:
                    self._ip_pool.remove(proxy)
                    break
                else:
                    yield from asyncio.sleep(0)
            else:
                yield from asyncio.sleep(0)
        return proxy.get("ip")

    def _proxy_success(self, proxy):
        pass

    def _proxy_missing(self):
        pass

    def _update_ip_pool(self, proxy):
        proxy = {
            'ip': proxy,
            'time': time.time()
        }
        self._ip_pool.append(proxy)
