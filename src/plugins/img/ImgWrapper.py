# -*- coding: utf-8 -*-
# create by yihui 10:16 19/1/22
import os
import random
import ssl
import time
from urllib import request

from PIL import Image

# 全局取消ssl校验
from src.logger.LoggerWrapper import SpiderLogger
from func_timeout import func_timeout, FunctionTimedOut

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


class ImgWrapper:
    def __init__(self):
        pass

    @staticmethod
    def tmp_save_with_timeout(url, app=None, timeout=5):
        try:
            return func_timeout(timeout, ImgWrapper.tmp_save, args=(url, app))
        except FunctionTimedOut:
            SpiderLogger.exception(f"tmp save img {url} timeout!\n")
            return None
        except Exception as e:
            SpiderLogger.exception(f"tmp save img {url} timeout!\n")
            return None

    @staticmethod
    def tmp_save(url, app=None):
        timestamp = int(time.time() * 1000)
        path = time.strftime("%Y-%m-%d", time.localtime(timestamp / 1000))
        if app:
            path = f"/tmp/img/{app}/{path}"
        else:
            path = f"/tmp/img/{path}"

        if not os.path.exists(path):
            # 当目录不存在时，主动创建
            os.makedirs(path)

        try:
            file = f"{path}/{timestamp}_{random.randint(0, 20)}"
            request.urlretrieve(url, file)
            return file
        except Exception as e:
            SpiderLogger.error("Faield to download img: {0}, {1}".format(url, e))
            return None

    @staticmethod
    def out_save_file(old_file, out_type, old_im, out_im):
        if not out_type:
            out_type = str(old_im.format).lower()

        if not out_type or out_type == 'webp':
            out_type = "jpg"

        out = old_file + "." + out_type
        out_im.save(out)
        return out

    @staticmethod
    def cut(url, app=None, w=None, h=None, x=None, y=None, output=None):
        """
        先将图片保存到本地，然后执行裁剪操作，最后输出指定格式的图片
        :param url: 图片链接, 可以是外部图片；也可以是本地图片
        :param app: 应用名，用于将下载和输出的图片聚类
        :param w: 裁剪之后的宽
        :param h: 裁剪之后的高
        :param x: x偏移
        :param y: y偏移
        :param output: 输出图片格式
        :return:
        """
        path = ImgWrapper.tmp_save(url, app)
        if not path:
            return None

        try:
            with Image.open(path) as im:
                img_w, img_h = im.size
                if not w or w > img_w:
                    w = img_w

                if not h or h > img_h:
                    h = img_h

                if not x:
                    # 没有指定x偏移，则居中裁剪
                    x = (img_w - w) / 2
                elif x + w > img_w:
                    # 避免裁后的图片比需要的小
                    x = img_w - w

                if not y:
                    y = (img_h - h) / 2
                elif y + h > img_h:
                    y = img_h - h

                ans = im.crop((x, y, w + x, h + y))
                return ImgWrapper.out_save_file(path, output, im, ans)
        except Exception as e:
            print("cut img error! url: {0}, e: {1}".format(url, e))
            SpiderLogger.error("cut img error! url: {0}, e: {1}".format(url, e))
            return None

    @staticmethod
    def cut_center(url, app=None, hw_rate=0.6, output=None):
        """
        居中，等比例裁剪
        :param url:
        :param app:
        :param hw_rate:
        :param output:
        :return:
        """
        path = ImgWrapper.tmp_save(url, app)
        if not path:
            return None

        try:
            with Image.open(path) as im:
                img_w, img_h = im.size
                w = img_w
                h = w * hw_rate

                x = 0
                y = (img_h - h) / 2
                ans = im.crop((x, y, w + x, h + y))
                return ImgWrapper.out_save_file(path, output, im, ans)
        except Exception as e:
            print("cut img error! url: {0}, e: {1}".format(url, e))
            SpiderLogger.error("cut img error! url: {0}, e: {1}".format(url, e))
            return None
