class AbstractProxy(object):
    def _pull_ips(self):
        """
        获取代理ip
        :return:
        """

        raise NotImplementedError

    def pop_proxy(self):
        """
        返回一个proxy
        :return:
        """
        raise NotImplementedError

    def _proxy_success(self, proxy):
        """
        获取成功
        :return:
        """
        raise NotImplementedError

    def _proxy_missing(self):
        """
        获取失败
        :return:
        """
        raise NotImplementedError

    def proxy_done(self, proxy, success=True):
        """
        获取完proxy执行
        :return:
        """
        self._update_ip_pool(proxy)
        if success:
            self._proxy_success(proxy)
        else:
            self._proxy_missing()

    def _update_ip_pool(self, proxy):
        """
        更新ip池
        :return:
        """
        raise NotImplementedError
