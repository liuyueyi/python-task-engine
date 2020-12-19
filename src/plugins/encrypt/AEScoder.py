# -*- coding: utf-8 -*-
# create by yihui 15:44 20/4/29

import base64
import hashlib
import random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from src.env.EnvWrapper import env_wrapper

BLOCK_SIZE = AES.block_size  # Bytes


class AEScoder:

    def __init__(self):
        self.salt = str(env_wrapper.get_conf("aes")['salt'])

    def encrypt(self, key, content, base64_encoder=True):
        """
        AES加密
        模式ecb
        填充pkcs5
        :param key: 密钥
        :param content: 加密内容
        :param base64_encoder
        :return:
        """
        key_bytes = bytes(key, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        # 加密
        if type(content) is str:
            content = content.encode("utf-8")
        encrypt_bytes = cipher.encrypt(pad(content, BLOCK_SIZE))
        if base64_encoder:
            # base64编码
            return str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        else:
            return encrypt_bytes

    def decrypt(self, key, content, base64_encoder=True, return_bytes=False):
        """
        AES解密
         key,iv使用同一个
        模式cbc
        去填充pkcs7
        :param key:
        :param content:
        :param base64_encoder: true 表示content为base64编码的格式，解密之前需要先解码
        :param return_bytes: true 表示返回byte；False表示返回String
        :return:
        """
        key_bytes = bytes(key, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        # base64解码
        # 解密
        if base64_encoder:
            encrypt_bytes = base64.b64decode(content)
        else:
            encrypt_bytes = content
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        if return_bytes:
            return unpad(decrypt_bytes, BLOCK_SIZE)
        else:
            # 重新编码
            return str(unpad(decrypt_bytes, BLOCK_SIZE), encoding='utf-8')

    def encrypt_cbc(self, key, iv, content, base64_encoder=True):
        """
        cbc 加密
        :param key:
        :param iv:
        :param content:
        :param base64_encoder:
        :return:
        """
        key = key[0:16]
        key_bytes = bytes(key, encoding='utf-8')
        iv_byes = bytes(iv, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_byes)
        # 加密
        if type(content) is str:
            content = content.encode("utf-8")
        encrypt_bytes = cipher.encrypt(pad(content, BLOCK_SIZE))
        if base64_encoder:
            # base64编码
            return str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        else:
            return encrypt_bytes

    def decrypt_cbc(self, key, iv, content, base64_encoder=True, return_bytes=False):
        """
        cbc 解密
        :param key:
        :param iv:
        :param content:
        :param base64_encoder:
        :return:
        """
        key = key[0:16]
        key_bytes = bytes(key, encoding='utf-8')
        iv_byes = bytes(iv, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_byes)
        # base64解码
        # 解密
        if base64_encoder:
            encrypt_bytes = base64.b64decode(content)
        else:
            encrypt_bytes = content
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        if return_bytes:
            return unpad(decrypt_bytes, BLOCK_SIZE)
        else:
            # 重新编码
            return str(unpad(decrypt_bytes, BLOCK_SIZE), encoding='utf-8')

    def parse_key_to_index(self, key, return_list=True):
        """
        将密钥解析为下标
        - key的排序规则：
            - key拆分为字符数组，根据ASCII码升序排列
            - 每个字符对应的数字，根据上面排序的下标来确定（如果一个字符存在多个下标时，采用队列规则，第一个出现的字符对应最后一个下标）
                - 举例说明: key = 62ef0cf8
                - 排序之后: 0 2 6 8 c e f f；
                - 字符下标: 0 -> 0;  2 -> 1;  6 -> 2;  8 -> 3;  c -> 4; e -> 5; f -> 6,7
                - 排序规则: 62ef0cf8 -> 21570463
        :param key:
        :param return_list:
        :return:
        """
        key_list = list(key)
        key_list.sort()
        mapper = {}
        index = -1
        for k in key_list:
            index = index + 1
            if k in mapper:
                mapper[k].append(index)
            else:
                mapper[k] = [index]

        if return_list:
            result = []
            for a in key:
                result.append(mapper[a].pop())
        else:
            result = {}
            index = 0
            for a in key:
                # key 为块真实地址， value为下标； 解密时使用
                result[mapper[a].pop()] = index
                index += 1

        return result

    def encrypt_pl(self, key, content):
        """
        自定义加密算法
        - 将content拆分为 len(key) + 1块， 前 len(key) = n块大小相同，最后一个块可以不同
        - 根据key，来确定前n块的排序规则，对这n个块进行重组，最后一块依然放在最后，得到加密后的字节数组
        - key的排序规则：
            - key拆分为字符数组，根据ASCII码升序排列
            - 每个字符对应的数字，根据上面排序的下标来确定（如果一个字符存在多个下标时，采用队列规则，第一个出现的字符对应最后一个下标）
                - 举例说明: key = 62ef0cf8
                - 排序之后: 0 2 6 8 c e f f；
                - 字符下标: 0 -> 0;  2 -> 1;  6 -> 2;  8 -> 3;  c -> 4; e -> 5; f -> 6,7
                - 排序规则: 62ef0cf8 -> 21570463
        :param key:
        :param content:
        :return:
        """
        cell_nums = len(key) + 1
        cell_size = int(len(content) / cell_nums)

        if cell_size <= 0:
            # 内容长度小于key长度，则不重组
            return content

        cell_index_array = self.parse_key_to_index(key)
        cells = []
        for i in range(0, cell_nums):
            index = i * cell_size
            if i == cell_nums - 1:
                # 最后一个
                cells.append(content[index:])
            else:
                cells.append(content[index: index + cell_size])

        res = b''
        for i in cell_index_array:
            res += cells[i]
        res += cells[-1]
        return res

    def decrypt_pl(self, key, content):
        """
        自定义解密算法
        :param key:
        :param content:
        :return:
        """
        cell_nums = len(key) + 1
        cell_size = int(len(content) / cell_nums)

        if cell_size <= 0:
            # 内容长度小于key长度，则不重组
            return content

        cells = []
        for i in range(0, cell_nums):
            index = i * cell_size
            if i == cell_nums - 1:
                # 最后一个
                cells.append(content[index:])
            else:
                cells.append(content[index: index + cell_size])

        cell_index_map = self.parse_key_to_index(key, False)
        ans = b''
        for index in range(0, cell_nums - 1):
            ans += cells[cell_index_map[index]]
        ans += cells[-1]
        return ans

    def show_key(self, n=16):
        """
        获取密钥 n 密钥长度
        :return:
        """
        c_length = int(n)
        source = 'QWERTYUIOPLKJHGFDSAZXCVBNM0123456789qwertyuioplkjhgfdsazxcvbnm'
        length = len(source) - 1
        result = ''
        for i in range(c_length):
            result += source[random.randint(0, length)]
        return result

    def real_key(self, encode_key: str):
        first = encode_key[0]
        if first.isdigit():
            index = int(first)
        else:
            index = 10 + ord(first.lower()) - 97

        if index > len(encode_key):
            content = encode_key + self.salt
        else:
            content = encode_key[0: index] + self.salt + encode_key[index:]

        return hashlib.md5(content.encode('utf-8')).hexdigest()


aes_coder = AEScoder()
