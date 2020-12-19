# -*- coding: utf-8 -*-
# create by yihui 16:53 20/5/8
import os

import requests
from requests.adapters import HTTPAdapter


def init_path(path):
    """
    初始化目录
    :param path:
    :return:
    """
    if not os.path.exists(path):
        # 当目录不存在时，主动创建
        os.makedirs(path)


def save_file(content: str, path: str, file_name):
    """
    文件保存
    :param content:
    :param path
    :param file_name:
    :return:
    """
    init_path(path)
    abs_file = path + file_name if path.endswith("/") else path + "/" + file_name
    with open(abs_file, 'w') as f:
        f.write(content)
        f.close()


s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


def read_into_buffer(filename, remote_uri=False):
    """
    将文件内容读取到字节数组中
    :param filename:
    :param remote_uri: true 表示网络资源； false表示本地资源
    :return:
    """
    if remote_uri:
        # 远程
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        resource = s.get(filename, headers=headers, verify=False, timeout=5)
        return resource.content
    else:
        # 本地小文件
        buf = bytearray(os.path.getsize(filename))
        with open(filename, 'rb') as f:
            f.readinto(buf)
        return bytes(buf)


def read_into_string(filename):
    """
    将文件按行读取
    :param filename:
    :return:
    """
    result = ''
    with open(filename, 'r') as f:
        for line in f.readlines():
            result += line

    return result
