# -*- coding: utf-8 -*-
# create by yihui 17:37 20/5/7
import zipfile
import zlib

import requests

from src.env.EnvWrapper import env_wrapper
from src.plugins.encrypt.AEScoder import aes_coder
from src.plugins.ios import FileUtil
from src.plugins.oss.aly.AliyunClient import aliyun_client
from src.plugins.oss.qiniu.QiniuClient import qiniu_client

CODE = "utf-8"


class UploadUtil:
    def __init__(self):
        self.conf_path = str(env_wrapper.get_conf("biz")['tmp_file'])
        if self.conf_path.startswith("/"):
            self.save_path = self.conf_path
        else:
            self.save_path = env_wrapper.get_module_path() + "/" + self.conf_path

    @staticmethod
    def split_path_name(up_file: str):
        index = up_file.rindex("/")
        if index > 0:
            return up_file[0:index], up_file[index + 1:]
        else:
            return "", up_file

    def save_file(self, upload_txt: str, save_file_name: str, prefix=None):
        """
        保存上传的文件到本地
        :param upload_txt:
        :param save_file_name:
        :param prefix:
        :return:
        """
        if prefix:
            upload_txt = prefix + upload_txt

        tmp_path, tmp_file = self.split_path_name(save_file_name)
        real_path = self.save_path + "/" + tmp_path
        FileUtil.save_file(upload_txt, real_path, tmp_file)

    def upload_to_qiniu(self, upload_txt: str, save_file_name: str, base_64_enable=False):
        """
        上传文件到七牛
        :param upload_txt: 上传的文本内容
        :param save_file_name: 保存的文件名
        :param base_64_enable: true 表示上传的文件是通过base64加密的
        :return:
        """
        # 保存原始文件
        self.save_file(upload_txt, save_file_name)

        # 生成编码key
        code_key = aes_coder.show_key()
        # 获取真实加密密钥
        real_key = aes_coder.real_key(code_key)
        # 压缩
        upload_bytes = upload_txt.encode(CODE)
        compress_bytes = zlib.compress(upload_bytes)
        # 加密
        if base_64_enable:
            zip_enc = aes_coder.encrypt(real_key, compress_bytes, True).encode(CODE)
        else:
            zip_enc = aes_coder.encrypt(real_key, compress_bytes, False)
        # 根据加密后的内容，计算crc校验码
        crc_code = zlib.crc32(zip_enc)
        # 上传
        file_uri = qiniu_client.upload_file(zip_enc, save_file_name)
        return {
            "code_key": code_key,
            "real_key": real_key,
            "novel_size": len(upload_txt),
            "crc32": crc_code,
            "file_uri": file_uri
        }

    def upload_to_qiniu_by_cbc(self, upload_txt: str, save_file_name: str, base_64_enable=False):
        """
        上传文件到七牛
        :param upload_txt: 上传的文本内容
        :param save_file_name: 保存的文件名
        :param base_64_enable: true 表示上传的文件是通过base64加密的
        :return:
        """
        # 生成编码key
        code_key = aes_coder.show_key()
        # 获取真实加密密钥
        real_key = aes_coder.real_key(code_key)
        # 压缩
        upload_bytes = upload_txt.encode(CODE)
        compress_bytes = zlib.compress(upload_bytes)
        # 加密
        if base_64_enable:
            zip_enc = aes_coder.encrypt_cbc(real_key, 'KD16-Byte-String', compress_bytes, True).encode(CODE)
        else:
            zip_enc = aes_coder.encrypt_cbc(real_key, 'KD16-Byte-String', compress_bytes, False)

        # 根据加密后的内容，计算crc校验码
        crc_code = zlib.crc32(zip_enc)
        # 上传
        file_uri = qiniu_client.upload_file(zip_enc, save_file_name)
        return {
            "code_key": code_key,
            "real_key": real_key,
            "novel_size": len(upload_txt),
            "crc32": crc_code,
            "file_uri": file_uri
        }

    def upload_to_qiniu_by_pl(self, upload_txt: str, save_file_name: str):
        """
        上传到七牛
        :param upload_txt:
        :param save_file_name:
        :return:
        """
        # 保存原始文件
        # self.save_file(upload_txt, save_file_name)
        # 生成编码key
        code_key = aes_coder.show_key()
        # 获取真实加密密钥
        real_key = aes_coder.real_key(code_key)
        # 压缩
        upload_bytes = upload_txt.encode(CODE)
        compress_bytes = zlib.compress(upload_bytes)
        # 加密
        zip_enc = aes_coder.encrypt_pl(real_key, compress_bytes)
        # 根据加密后的内容，计算crc校验码
        crc_code = zlib.crc32(zip_enc)
        # 上传
        file_uri = qiniu_client.upload_file(zip_enc, save_file_name)
        return {
            "code_key": code_key,
            "real_key": real_key,
            "novel_size": len(upload_txt),
            "crc32": crc_code,
            "file_uri": file_uri
        }

    @staticmethod
    def simple_upload_to_aliyun(upload_txt: str, save_file_name: str):
        """
        原文上传
        :param upload_txt: 上传的文本
        :param save_file_name:
        :return:
        """
        file_uri = aliyun_client.upload_novel(upload_txt, save_file_name, "txt")
        crc_code = zlib.crc32(upload_txt.encode(CODE))
        return {
            'crc32': crc_code,
            'file_url': file_uri
        }

    def upload_to_aliyun_by_pl(self, upload_txt: str, save_file_name: str, bucket="novel", save_file=True):
        """
        上传到阿里云
        :param upload_txt:
        :param save_file_name:
        :param bucket: 文件上传的bucket, 默认为看点的novel
        :return:
        """
        # 保存原始文件
        if save_file:
            self.save_file(upload_txt, save_file_name)

        # 生成编码key
        code_key = aes_coder.show_key()
        # 获取真实加密密钥
        real_key = aes_coder.real_key(code_key)
        # 压缩
        upload_bytes = upload_txt.encode(CODE)
        compress_bytes = zlib.compress(upload_bytes)
        # 加密
        zip_enc = aes_coder.encrypt_pl(real_key, compress_bytes)
        # 根据加密后的内容，计算crc校验码
        crc_code = zlib.crc32(zip_enc)
        # 上传
        file_uri = aliyun_client.upload_novel(zip_enc, save_file_name, "bytes", bucket=bucket)
        return {
            "code_key": code_key,
            "real_key": real_key,
            "novel_size": len(upload_txt),
            "crc32": crc_code,
            "file_uri": file_uri
        }

    def dow_origin_nove_by_pl(self, file_uri: str, code_key: str):
        """
        下载并解密解压小说内容
        :param file_uri:
        :param code_key:
        :return:
        """
        resource = requests.get(file_uri, verify=False)
        down_bytes = resource.content
        # 计算真实密钥
        real_key = aes_coder.real_key(code_key)
        # 解密，并返回字节数组
        decode_bytes = aes_coder.decrypt_pl(real_key, down_bytes)
        # 解压
        uncompress_bytes = zlib.decompress(decode_bytes)
        return uncompress_bytes.decode(CODE)

    def dow_origin_nove_by_cbc(self, file_uri: str, code_key: str, base_64_enable=False):
        """
        下载并解密解压小说内容
        :param file_uri:
        :param code_key:
        :param base_64_enable:
        :return:
        """
        resource = requests.get(file_uri)
        down_bytes = resource.content
        # 计算真实密钥
        real_key = aes_coder.real_key(code_key)
        # 解密，并返回字节数组
        decode_bytes = aes_coder.decrypt_cbc(real_key, 'KD16-Byte-String', down_bytes, base_64_enable, True)
        # 解压
        uncompress_bytes = zlib.decompress(decode_bytes)
        return uncompress_bytes.decode(CODE)

    def dow_origin_novel(self, file_uri: str, code_key: str, base_64_enable=False):
        """
        下载并解密解压小说内容
        :param file_uri:
        :param code_key:
        :param base_64_enable:
        :return:
        """
        resource = requests.get(file_uri)
        down_bytes = resource.content
        # 计算真实密钥
        real_key = aes_coder.real_key(code_key)
        # 解密，并返回字节数组
        decode_bytes = aes_coder.decrypt(real_key, down_bytes, base_64_enable, True)
        # 解压
        uncompress_bytes = zlib.decompress(decode_bytes)
        return uncompress_bytes.decode(CODE)

    @staticmethod
    def up_compress_novel(content):
        compress_bytes = zlib.compress(content)
        file_uri = qiniu_client.upload_file(compress_bytes, "compress/test.d")
        return file_uri

    @staticmethod
    def get_zip(files, zip_name):
        zp = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zp.write(file, "origin.txt")
        zp.close()

    @staticmethod
    def up_zip_novel(content):
        filename = "/tmp/test.zip"
        tmp_save = "/tmp/origin.txt"
        UploadUtil.save(content, tmp_save)
        UploadUtil.get_zip([tmp_save], filename)

    @staticmethod
    def save(content, file):
        with open(file, "w") as f:
            f.write(content)
            f.flush()

    @staticmethod
    def uncompress_novel(url):
        resource = requests.get(url)
        down_bytes = resource.content
        uncompress_bytes = zlib.decompress(down_bytes)
        return uncompress_bytes.decode(CODE)


upload_util = UploadUtil()
