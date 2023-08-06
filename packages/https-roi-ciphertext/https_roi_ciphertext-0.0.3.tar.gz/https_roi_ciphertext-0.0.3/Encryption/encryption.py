"""
    @File : encryption.py 
    @Create : 2021/11/23 上午9:27 
    @Author : wx
    @Update : 2021/11/23 上午9:27 
    @License : (C)Copyright 2014-2021 SmartAHC All Rights Reserved 
    @Desc    :   Coding Below
    @Software: PyCharm
"""

"""
实现非对称加密:
    1. 使用Crypto中RSA算法
    2. 生成公钥和私钥文件
    3. 加密、解密
        1. 实现公钥加密，私钥解密
        2. 私钥生成签名, 公钥验证签名
    4. 生成签名 哈希hash  md5
    5. 验证加密数据和签名
"""

import os

from Crypto.Cipher.PKCS1_v1_5 import new
from Crypto.PublicKey import RSA
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from binascii import a2b_hex


# 获取客户端的 公钥和私钥（非配对密钥）
def key_init():
    key = b'\x9c1\xf9g?P\xd3T\t\xe2\xc8\x03\x8d\xde\x15]'
    mode = AES.MODE_OFB

    # 获取客户端公钥 and # 获取客户端私钥
    pub_key = get_key()
    if pub_key:
        # 导出正规的密钥密码

        pri_key = RSA.importKey(base64.b64decode(pub_key))
        # self.pub_key_obj = Cipher_pkcs1_v1_5.new(pri_key)
        pub_key_obj = new(pri_key, b'M')
    else:
        raise ValueError("密钥不存在")
    return key, mode, pub_key, pub_key_obj


# 获取密钥
def get_key():
    path = os.getcwd() + "/pem_file/cli_public_pem.pem"
    pu_key = open(path, 'r').readlines()
    return ''.join(pu_key[1:-1])


# 公钥加密
def public_long_encrypt(data, charset='utf-8'):
    # 使用服务端私钥和数据生成签名
    key, mode, pub_key, pub_key_obj = key_init()
    data = str(data).encode(charset)
    length = len(data)
    default_length = 117  # 加密数据最小长度对117
    res = []
    for i in range(0, length, default_length):
        res.append(pub_key_obj.encrypt(data[i:i + default_length]))
    byte_data = b''.join(res)
    return base64.b64encode(byte_data)


# 使用公钥验证签名
def verify_sign(signature, message, charset='utf-8'):
    key, mode, pub_key, pub_key_obj = key_init()
    message = str(message).encode(charset)
    key = RSA.importKey(base64.b64decode(pub_key))
    h = SHA.new(message)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature):
        print("The signature is authentic.")
        return True
    else:
        print("The signature is not authentic.")
        return False


# 公共密钥解密
def private_long_decrypt(encryption_data, message):
    try:
        key, mode, pub_key, pub_key_obj = key_init()
        cryptor = AES.new(key, mode, key)
        plain_text = cryptor.decrypt(a2b_hex(base64.b64decode(encryption_data.get("data").get("encrypt_data"))))
        data = eval(plain_text.decode('utf-8').rstrip('\0'))
        sign = data['sign']
        result = verify_sign(sign, message)
        if result:
            return data
        else:
            return {"error": "The signature is not authentic."}
    except Exception as e:
        print(e)
        return {"error": "decrypt failed"}
