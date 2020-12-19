# -*- coding: utf-8 -*-
# create by yihui 11:47 19/11/25

"""
钉钉报警
"""
import asyncio
import datetime
import json
import socket

import aiohttp

from src.env.EnvWrapper import env_wrapper
from src.logger.LoggerWrapper import SpiderLogger

# 默认的钉钉报警群
DEFAULT_URL = ''

FEISHU_URL = ''


async def ding_talk_sender_by_url(message, url=DEFAULT_URL):
    robot_url = url
    text_message = dict()
    text_message['msgtype'] = 'text'
    env = "线下" if env_wrapper.is_debug() else "线上"
    text_message['text'] = {
        'content': "JokeSpider-【{0}】[{1}] \n{2}".format(env, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                        message)
    }
    headers = {'Content-Type': 'application/json'}
    try:
        session = aiohttp.ClientSession()
        resp = await session.post(robot_url, timeout=10, headers=headers, data=json.dumps(text_message), ssl=False)
        raw = await resp.text("utf-8", "ignore")
        SpiderLogger.info(f"返回结果: {raw}")
        resp.close()
        await session.close()
    except asyncio.CancelledError:
        SpiderLogger.error("尚有未发送的严重告警:{}".format(message))
        raise asyncio.CancelledError


async def feishu_by_url(title, message, token=FEISHU_URL):
    robot_url = token
    text_message = {
        'title': "【" + socket.gethostname() + "】" + title,
        "text": message
    }

    headers = {'Content-Type': 'application/json'}
    try:
        session = aiohttp.ClientSession()
        resp = await session.post(robot_url, timeout=10, headers=headers, data=json.dumps(text_message), ssl=False)
        raw = await resp.text("utf-8", "ignore")
        resp.close()
        await session.close()
    except asyncio.CancelledError:
        SpiderLogger.error("尚有未发送的严重告警:{}".format(message))
        raise asyncio.CancelledError


async def feishu_v2(title, message, token=''):
    message = {
        'msg_type': 'post',
        'content': {
            'post': {
                'zh_cn': {
                    'title': title,
                    'content': [message]
                }
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    try:
        session = aiohttp.ClientSession()
        resp = await session.post(token, timeout=10, headers=headers, data=json.dumps(message), ssl=False)
        raw = await resp.text("utf-8", "ignore")
        SpiderLogger.info(f"feishu res: {raw}")
        resp.close()
        await session.close()
    except asyncio.CancelledError:
        SpiderLogger.error("尚有未发送的严重告警:{}".format(message))
        raise asyncio.CancelledError
