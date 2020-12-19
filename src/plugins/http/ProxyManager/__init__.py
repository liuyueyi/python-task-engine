import asyncio
from enum import unique, Enum

from src.plugins.logger.LoggerWrapper import SpiderLogger
from src.plugins.http.ProxyManager.Impls.FixedProxy import FixedProxy
from src.plugins.http.ProxyManager.Impls.SocksProxy import SocksProxy

__proxy_inst = None
# true 表示全局代理
__global = False


@unique
class ProxyState(Enum):
    GLOBAL = 'global'
    NO_PROXY = 'no'
    SPECIAL_PROXY = 'special'


def init_proxy(use_proxy, global_proxy=True):
    global __proxy_inst
    global __global

    if __proxy_inst:
        return None

    if use_proxy == "socks":
        __proxy_inst = SocksProxy()
        __global = global_proxy
    elif use_proxy == "fixed":
        SpiderLogger.get_logger().info("动态代理已启用")
        __proxy_inst = FixedProxy()
        __global = global_proxy


@asyncio.coroutine
def pop_proxy(global_pop=True):
    global __global
    if __global == global_pop and __proxy_inst is not None:
        return (yield from __proxy_inst.pop_proxy())


@asyncio.coroutine
def pop_proxy_by_state(state: ProxyState):
    global __proxy_inst
    global __global
    if state == ProxyState.NO_PROXY:
        # 不走代理，直接返回None
        return None
    elif state == ProxyState.GLOBAL:
        # 全局代理获取时，首先判断是否开启了全局代理，若开启则返回代理ip；否则返回None
        if __global:
            return (yield from __proxy_inst.pop_proxy())
        else:
            return None
    elif state == ProxyState.SPECIAL_PROXY:
        # 强制开启代理，若代理池已经初始化，则直接返回；否则初始化
        if __proxy_inst:
            return (yield from __proxy_inst.pop_proxy())
        else:
            init_proxy("fixed", False)
            return (yield from __proxy_inst.pop_proxy())


def proxy_done(proxy, success=True):
    if __proxy_inst is not None:
        return __proxy_inst.proxy_done(proxy, success)
