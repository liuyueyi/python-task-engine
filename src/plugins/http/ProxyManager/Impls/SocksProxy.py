import asyncio

from src.plugins.http.ProxyManager.AbstractProxy import AbstractProxy


class SocksProxy(AbstractProxy):
    def __init__(self):
        self.socks_ip = ["http://192.168.0.1:1080"]

    @asyncio.coroutine
    def pop_proxy(self):
        return self.socks_ip[0]

    def _proxy_success(self, proxy):
        pass

    def _proxy_missing(self):
        pass

    def _update_ip_pool(self, proxy):
        pass

    def _pull_ips(self):
        pass
