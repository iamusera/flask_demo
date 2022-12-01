# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64


def decrypt(encrypt_str, security_key):
    """
    解密
    :param encrypt_str: 加密字符串
    :param security_key: 密钥
    :return: 解密后字符
    """
    key = base64.b64decode(security_key)
    cryptor = AES.new(key, AES.MODE_ECB)
    s = base64.b64decode(encrypt_str)
    s = cryptor.decrypt(s)
    s = bytes.decode(s)
    s = s.strip().rstrip().replace("\b", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("",
                                                                                                           "").replace(
        "\x07", "")
    return s


if __name__ == "__main__":
    s = decrypt("foUpRHA0pzNU0hH7hyotYg==", "S0FJWVVEU1NQTE04ODg4OA==")
    print(s)
