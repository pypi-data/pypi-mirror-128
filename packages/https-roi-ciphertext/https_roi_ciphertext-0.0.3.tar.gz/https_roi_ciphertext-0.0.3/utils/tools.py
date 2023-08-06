"""
    @File : tools.py 
    @Create : 2021/11/23 上午9:29 
    @Author : wx
    @Update : 2021/11/23 上午9:29 
    @License : (C)Copyright 2014-2021 SmartAHC All Rights Reserved 
    @Desc    :   Coding Below
    @Software: PyCharm
"""
import os

from Crypto.Cipher.PKCS1_v1_5 import PKCS115_Cipher
from Crypto.PublicKey import RSA
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 生成密码文件
class CreateClientPemKey():
    """
    1. 生成密钥长度为1024位的私钥（RsaKey对象）  标准仅定义了1024、2048和3072 推荐使用2048
    2. 其二进制位长度可以是1024位或者2048位.长度越长其加密强度越大,目前为止公之于众的能破解的最大长度为768位密钥,只要高于768位,相对就比较安全.所以目前为止,这种加密算法一直被广泛使用.
    """

    def __init__(self):
        self.key = RSA.generate(1024)

    # 生成私钥文件
    def private_pem(self):
        private_pem = self.key.export_key().decode()
        with open('../pem_file/ser_private_pem.pem', 'w') as pr:
            pr.write(private_pem)

    # 生成公钥文件
    def public_pem(self):
        public_key = self.key.publickey()
        public_pem = public_key.export_key().decode()
        with open('../pem_file/cli_public_pem.pem', 'w') as pu:
            pu.write(public_pem)

    def start(self):
        self.public_pem()
        self.private_pem()


class ClientEncryptionTool():
    # 获取客户端的 公钥和私钥（非配对密钥）
    def __init__(self):
        self.key = b'\x9c1\xf9g?P\xd3T\t\xe2\xc8\x03\x8d\xde\x15]'
        self.mode = AES.MODE_OFB

        # 获取客户端公钥 and # 获取客户端私钥
        self.pub_key = self.get_key()
        if self.pub_key:
            # 导出正规的密钥密码

            pri_key = RSA.importKey(base64.b64decode(self.pub_key))
            # self.pub_key_obj = Cipher_pkcs1_v1_5.new(pri_key)
            self.pub_key_obj = new(pri_key, b'M')
        else:
            raise ValueError("密钥不存在")

    # 获取密钥
    def get_key(self, ):
        path = os.getcwd() + "/pem_file/cli_public_pem.pem"
        pu_key = open(path, 'r').readlines()
        return ''.join(pu_key[1:-1])

    # 公钥加密
    def public_long_encrypt(self, data, charset='utf-8'):
        # 使用服务端私钥和数据生成签名
        data = str(data).encode(charset)
        length = len(data)
        default_length = 117  # 加密数据最小长度对117
        res = []
        for i in range(0, length, default_length):
            res.append(self.pub_key_obj.encrypt(data[i:i + default_length]))
        byte_data = b''.join(res)
        return base64.b64encode(byte_data)

    # 使用公钥验证签名
    def verify_sign(self, signature, message, charset='utf-8'):
        message = str(message).encode(charset)
        key = RSA.importKey(base64.b64decode(self.pub_key))
        h = SHA.new(message)
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(h, signature):
            print("The signature is authentic.")
            return True
        else:
            print("The signature is not authentic.")
            return False

    # 公共密钥解密
    def private_long_decrypt(self, encryption_data, message):
        try:
            cryptor = AES.new(self.key, self.mode, self.key)
            plain_text = cryptor.decrypt(a2b_hex(base64.b64decode(encryption_data.get("data").get("encrypt_data"))))
            data = eval(plain_text.decode('utf-8').rstrip('\0'))
            sign = data['sign']
            result = self.verify_sign(sign, message)
            if result:
                return data
            else:
                return {"error": "The signature is not authentic."}
        except Exception as e:
            print(e)
            return {"error": "decrypt failed"}


from Crypto.Util.number import ceil_div, bytes_to_long, long_to_bytes
from Crypto.Util.py3compat import bord, _copy_bytes
import Crypto.Util.number


class RewriteEncrypt(PKCS115_Cipher):
    def encrypt(self, message):
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        mLen = len(message)

        if mLen > k - 11:
            raise ValueError("Plaintext is too long.")

        ps = []
        while len(ps) != k - mLen - 3:
            new_byte = self._randfunc
            if bord(new_byte[0]) == 0x00:
                continue
            ps.append(new_byte)
        ps = b"".join(ps)
        assert (len(ps) == k - mLen - 3)

        em = b'\x00\x02' + ps + b'\x00' + _copy_bytes(None, None, message)
        em_int = bytes_to_long(em)
        m_int = self._key._encrypt(em_int)
        c = long_to_bytes(m_int, k)
        return c


def new(key, randfunc):
    return RewriteEncrypt(key, randfunc)
