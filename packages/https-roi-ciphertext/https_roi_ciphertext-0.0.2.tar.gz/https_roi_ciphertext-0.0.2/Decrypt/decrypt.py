"""
    @File : server_encryption.py 
    @Create : 2021/7/8 下午5:24 
    @Author : wx
    @Update : 2021/7/8 下午5:24 
    @License : (C)Copyright 2014-2021 SmartAHC All Rights Reserved 
    @Desc    :   Coding Below
    @Software: PyCharm
"""

import os
from Crypto.PublicKey import RSA
from Crypto.Cipher.PKCS1_v1_5 import new
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from binascii import b2a_hex


class ServerDecryptTool():
    # 获取客户端的 公钥和私钥（非配对密钥）
    def __init__(self):
        # 获取客户端私钥
        self.key = b'\x9c1\xf9g?P\xd3T\t\xe2\xc8\x03\x8d\xde\x15]'
        self.mode = AES.MODE_OFB
        self.pri_key = self.get_key()
        if self.pri_key:
            # 导出正规的密钥密码
            pri_key = RSA.importKey(base64.b64decode(self.pri_key))
            # self.pub_key_obj = Cipher_pkcs1_v1_5.new(pri_key)
            self.pri_key_obj = new(pri_key, b'M')
        else:
            raise ValueError("密钥不存在")

    # 获取密钥
    def get_key(self):
        path = os.getcwd() + "/pem_file/ser_private_pem.pem"
        pri_key = open(path, 'r').readlines()
        return ''.join(pri_key[1:-1])

    # 生成签名
    def get_sign(self, message, charset='utf-8'):
        message = str(message).encode(charset)
        pri_key = RSA.importKey(base64.b64decode(self.pri_key))
        h = SHA.new(message)
        signer = PKCS1_v1_5.new(pri_key)
        signature = signer.sign(h)
        return signature

    # 公共密钥加密
    def aes_encrypt(self, data):
        # 使用服务端私钥和数据生成签名
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(data)
        if count % length != 0:
            add = length - (count % length)
        else:
            add = 0

        message = str(data) + ('\0' * add)
        ciphertext = cryptor.encrypt(message.encode('utf-8'))
        result = b2a_hex(ciphertext)
        print(result)
        return base64.b64encode(result)

    # 私钥解密
    def private_long_decrypt(self, data, sentinel=b'decrypt error'):
        try:
            data = base64.b64decode(data)
            length = len(data)
            default_length = 128
            res = []
            for i in range(0, length, default_length):
                res.append(self.pri_key_obj.decrypt(data[i:i + default_length], sentinel))
            data = eval(str(b''.join(res), encoding="utf-8"))
            return data
        except Exception as e:
            print(e)
            return {"error": "decrypt failed"}
