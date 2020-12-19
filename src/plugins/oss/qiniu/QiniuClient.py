# -*- coding: utf-8 -*-
# create by yihui 14:19 20/4/29

from qiniu import Auth, put_data, put_file
import requests
import hashlib

from src.env.EnvWrapper import env_wrapper


class QiniuClient:
    """
    七牛云客户端, 全局单例
    """
    HTTP_SCHEMA = "https"
    # 上传类型
    UPLOAD_IMG = "image"
    UPLOAD_VIDEO = "video"
    UPLOAD_FILE = "file"

    def __init__(self):
        self._client = None
        self._bucket_name = None
        self._prefix = None
        self.init()

    def init(self, key='qiniu'):
        """
        :return:
        """
        qiniu_conf = env_wrapper.get_conf(key)
        self._client = Auth(qiniu_conf['ak'], qiniu_conf['sk'])
        self._bucket_name = qiniu_conf['bucket']
        self._prefix = qiniu_conf['prefix']

    @property
    def prefix(self):
        return self._prefix

    def get_full_path(self, path):
        if path.startswith(self.HTTP_SCHEMA):
            return path
        return "{}{}".format(self.prefix, path)

    def upload_file(self, data, file_key):
        """
        上传文件
        :param data: 上传的二进制数据
        :param file_key: 保存的文件名
        :return:
        """
        upload_token = self._client.upload_token(self._bucket_name, file_key)
        _, info = put_data(upload_token, file_key, data)
        if info.status_code != 200:
            raise Exception("上传文件失败!")
        return self.http2https(file_key)

    def upload_local_file(self, data_type, file_path):
        md5 = self.get_file_md5(file_path)
        file_key = "{}/{}".format(data_type, md5)
        upload_token = self._client.upload_token(self._bucket_name, file_key)
        _, info = put_file(upload_token, file_key, file_path)
        if info.status_code != 200:
            raise Exception("上传文件失败!")
        return self.http2https(file_key)

    async def upload_remote_file(self, data_type, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.87 Safari/537.36'
        }
        resp = requests.get(url, headers=headers).content
        md5 = hashlib.md5(resp).hexdigest()
        file_key = "{}/{}".format(data_type, md5)
        return self.upload_file(resp, file_key)

    @staticmethod
    def get_file_md5(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        while True:
            d = f.read(8096)
            if not d:
                break
            md5_obj.update(d)
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5

    def http2https(self, url: str):
        """
        将http开头的url改成https开头的url
        :param url:
        :return:
        """
        if url.startswith("https:"):
            return url
        elif url.startswith("http:"):
            return "https:" + url[5:]
        else:
            return self.prefix + url


qiniu_client = QiniuClient()
init = qiniu_client.init
upload_remote_file = qiniu_client.upload_remote_file
upload_local_file = qiniu_client.upload_local_file
get_full_path = qiniu_client.get_full_path
