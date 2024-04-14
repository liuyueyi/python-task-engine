# -*- coding: utf-8 -*-
# create by yihui 15:17 18/12/20

import asyncio
import json
import ssl
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup

from src.plugins.http.ProxyManager import proxy_done, ProxyState, pop_proxy_by_state
from src.plugins.logger.LoggerWrapper import SpiderLogger

# 忽略https证书校验
ssl._create_default_https_context = ssl._create_unverified_context


class ResultType(Enum):
    STR = 'str'
    JSON = 'json'
    PAGE = 'page'
    DEFAULT = 'default'


async def safe_requests(url, method='get', timeout=20, max_retry=1, retry_sleep=10, ignore_encoding_error=False,
                        mode='aiohttp', user_agent='', html_charset=None, result_type=ResultType.DEFAULT, **kwargs):
    """
    安全的获得链接返回的内容
    :param mode: 默认使用aiohttp发送器，分别有scrape、phantomjs
    :param url:
    :param method:
    :param timeout:
    :param max_retry:
    :param retry_sleep:
    :param html_charset 网页编码
    :param ignore_encoding_error
    :param user_agent: 代理
    :param result_type: 返回结果类型
    :param kwargs:
    :return:
    """
    if 'ssl' not in kwargs:
        kwargs['ssl'] = False

    if 'headers' not in kwargs:
        headers = {}
    else:
        headers = kwargs['headers']
        del kwargs['headers']

    if not user_agent:
        headers[
            'user-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/67.0.3396.87 Safari/537.36'
    else:
        headers['user-agent'] = user_agent

    # 设置代理状态，然后将传入参数干掉
    if 'proxy_enable' not in kwargs.keys():
        proxy_state = ProxyState.GLOBAL
    elif kwargs['proxy_enable']:
        proxy_state = ProxyState.SPECIAL_PROXY
        del kwargs['proxy_enable']
    else:
        proxy_state = ProxyState.NO_PROXY
        del kwargs['proxy_enable']

    # 设置cookies，然后将cookies从传参中删掉
    if 'cookies' not in kwargs:
        in_cookies = None
    else:
        in_cookies = kwargs['cookies']
        del kwargs['cookies']

    async def session_get():

        session = aiohttp.ClientSession(cookies=in_cookies)
        try:
            if method.lower() == 'get':
                response = await session.get(url, timeout=timeout, proxy=proxy, headers=headers, **kwargs)
            else:
                # 对于post 请求， data=xxx 用于表单请求场景； json = xxx 用于json传参方式请求
                assert method.lower() == 'post', "不支持get, post外的请求，请检查代码"
                response = await session.post(url, timeout=timeout, proxy=proxy, headers=headers, **kwargs)
            if ignore_encoding_error:
                raw = await response.text(response.charset, "ignore")
            else:
                if html_charset:
                    code = html_charset
                elif response.charset == 'gb2312':
                    code = 'gbk'
                else:
                    code = response.charset
                raw = await response.text(encoding=code)
            proxy_done(proxy, success=True)
            return raw
        finally:
            await session.close()

    if mode == 'aiohttp':
        mode_method = session_get()
    else:
        raise Exception('请求方式错误，只有aiohttp、phantomjs、scrape三种请求方式')
    retry = max_retry
    while retry > 0:
        proxy = await pop_proxy_by_state(proxy_state)
        if proxy:
            print("代理为: " + str(proxy))
        try:
            result = await mode_method
            if not result or result_type == ResultType.DEFAULT:
                return result

            if result_type == ResultType.STR:
                return str(result)
            elif result_type == ResultType.PAGE:
                return BeautifulSoup(result, 'html.parser')
            elif result_type == ResultType.JSON:
                return json.loads(result)
            else:
                return result
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            retry -= 1
            proxy_done(proxy, success=False)
            _ = ex
            SpiderLogger.exception("请求{}失败,重试中({})".format(url, retry))
            await asyncio.sleep(retry_sleep)
    if retry == 0:
        SpiderLogger.error("重试超时, 请求{}已失败!".format(url))
