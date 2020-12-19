# -*- coding: utf-8 -*-
# create by yihui 14:13 20/5/11
import hashlib
import imghdr

import oss2
import requests
from func_timeout import func_timeout, FunctionTimedOut

from src.env.EnvWrapper import env_wrapper
from src.logger.LoggerWrapper import SpiderLogger
from src.plugins.ios.FileUtil import read_into_buffer


class AliyunClient:
    """
    七牛云客户端, 全局单例
    """
    HTTP_SCHEMA = "https"
    # 上传类型
    UPLOAD_IMG = "img"
    UPLOAD_NOVEL = "novel"
    UPLOAD_COMIC = "comic"

    def __init__(self):
        self._auth = None
        self._bucket_name = None
        self.buckets = {}
        self.init()

    def init(self, key='aliyun'):
        """
        :return:
        """
        aliyun_conf = env_wrapper.get_conf(key)
        self._auth = oss2.Auth(aliyun_conf['ak'], aliyun_conf['sk'])
        for key, bucket in aliyun_conf['buckets'].items():
            endpoint = bucket['endpoint']
            bucket_name = bucket['bucket']
            oss_host = bucket['host']

            self.buckets[key] = {
                'client': oss2.Bucket(self._auth, endpoint, bucket_name),
                'host': oss_host
            }

        pass

    def upload_img_with_timeout(self, data, save_name=None, prefix='', data_type='file', timeout=60):
        try:
            return func_timeout(timeout, self.upload_img, args=(data, save_name, prefix, data_type))
        except FunctionTimedOut:
            SpiderLogger.exception(f"tmp upload img {data} timeout!\n")
            return None
        except Exception as e:
            SpiderLogger.exception(f"tmp upload img {data} error!\n")
            return None

    def upload_img(self, data, save_name=None, prefix='', data_type='file', bucket="img"):
        """
        上传图片, 仅支持本地和远程两种上传方式，图片名根据md5进行计算
        :param data:
        :param save_name: 如果非空，则表示指定了上传的图片名；如果为空，则上传的图片名为: prefix + md5
        :param prefix:
        :param data_type:
        :return:
        """
        bucket_info = self.buckets[bucket]
        if data_type == 'file':
            up_bytes = read_into_buffer(data, False)
        else:
            up_bytes = read_into_buffer(data, True)

        if not save_name:
            md5 = hashlib.md5(up_bytes).hexdigest()
            if prefix.endswith("/"):
                file_key = "{}{}".format(prefix, md5)
            else:
                file_key = "{}/{}".format(prefix, md5)
        else:
            file_key = save_name

        headers = dict()
        img_type = imghdr.what(None, up_bytes)
        headers['Content-Type'] = 'image/' + (img_type if img_type else 'jpeg')
        result = bucket_info['client'].put_object(file_key, up_bytes, headers=headers)
        oss_url = self.get_full_path(bucket_info['host'], file_key)
        SpiderLogger.info(f"upload {oss_url}  rqid: {result.request_id}", "aliyun")
        return oss_url

    def upload_comic(self, data, save_name, referer,
                     user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'):
        """
        漫画上传
        :param data:
        :param save_name:
        :param data_type:
        :return:
        """
        bucket_info = self.buckets['comic']
        headers = {
            'User-Agent': user_agent,
            'Referer': referer
        }
        try:
            input = requests.get(data, headers=headers, timeout=5)
        except Exception as e:
            SpiderLogger.info(f"get {data} timeout!")
            return None
        if input.status_code != 200 or len(input.content) < 1000:
            return None

        result = bucket_info['client'].put_object(save_name, input)
        oss_url = self.get_full_path(bucket_info['host'], save_name)
        SpiderLogger.info(f"upload {oss_url}  rqid: {result.request_id}", "aliyun")
        return oss_url

    def upload_novel(self, data, save_name, data_type='txt', bucket="novel"):
        """
        上传小说
        :param data:
        :param save_name:
        :param data_type: 上传的方式
        :param bucket: 上传的oss bucket，默认为看点novel, 可以主动设置为其他
        :return:
        """
        bucket_info = self.buckets[bucket]
        return self.__do_upload(bucket_info, data, save_name, data_type)

    def __do_upload(self, bucket_info, data, save_name, data_type):
        """
        具体的执行上传操作
        :param bucket_info:
        :param data:
        :param save_name:
        :param data_type:
        :return:
        """
        if data_type == 'txt':
            # 纯文本上传
            result = bucket_info['client'].put_object(save_name, data)
        elif data_type == 'bytes':
            # 二进制数组上传
            result = bucket_info['client'].put_object(save_name, data)
        elif data_type == 'file':
            # 本地文件上传
            result = bucket_info['client'].put_object_from_file(save_name, data)
        elif data_type == 'url':
            # 远程文件上传
            input = requests.get(data)
            result = bucket_info['client'].put_object(save_name, input)

        oss_url = self.get_full_path(bucket_info['host'], save_name)
        SpiderLogger.info(f"upload {oss_url}  rqid: {result.request_id}", "aliyun")
        return oss_url

    def get_full_path(self, host, path):
        """
        获取完整的url
        :param host:
        :param path:
        :return:
        """
        if path.startswith(self.HTTP_SCHEMA):
            return path
        if path.startswith("/"):
            return "{}{}".format(host, path)
        else:
            return "{}/{}".format(host, path)

    def http2https(self, host: str, url: str):
        """
        将http开头的url改成https开头的url
        :param host:
        :param url:
        :return:
        """
        if url.startswith("https:"):
            return url
        elif url.startswith("http:"):
            return "https:" + url[5:]
        else:
            return self.get_full_path(host, url)


aliyun_client = AliyunClient()
