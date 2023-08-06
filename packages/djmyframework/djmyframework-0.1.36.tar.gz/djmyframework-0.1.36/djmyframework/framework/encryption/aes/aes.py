import os
import sys
import base64
import json

from Crypto import Random
from Crypto.Cipher import AES


class AESCrypt:
    """
    AES/ECB/PKCS#7 加密算法
    AES/ECB/PKCS#5 加密算法

    AES/CBC/PKCS#7 加密算法
    AES/CBC/PKCS#5 加密算法

    支持:
    AES.MODE_CBC
    AES.MODE_ECB
    """
    BLOCK_SIZE = 16

    PKCS5_PAD = 'PKCS5'
    PKCS7_PAD = 'PKCS7'

    def __init__(self, secret_key, iv=None, aes_mode=AES.MODE_CBC, pad_mode=PKCS7_PAD):

        if not iv:
            iv = Random.new().read(AES.block_size)
        elif isinstance(iv, str):
            iv = iv.encode('utf-8')
        elif isinstance(iv, bytes):
            pass

        if len(iv) != 16:
            raise ValueError('iv长度错误')

        self.aes_mode = aes_mode
        self.pad_mode = pad_mode
        self.secret_key = secret_key.encode('utf-8')
        self.iv = iv

        if not secret_key or (len(secret_key) == 0):
            raise ValueError('密钥长度错误')

    def pkcs5_pad(self, s):
        """
        padding to blocksize according to PKCS #5
        calculates the number of missing chars to BLOCK_SIZE and pads with
        ord(number of missing chars)
        @see: http://www.di-mgt.com.au/cryptopad.html
        @param s: string to pad
        @type s: string
        @rtype: string
        """
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

    def pkcs5_unpad(self, s):
        """
        unpadding according to PKCS #5
        """
        return s[0:-ord(s[-1])]

    def pkcs7_pad(self, s):
        length = self.BLOCK_SIZE - (len(s) % self.BLOCK_SIZE)
        s += bytes([length]) * length
        return s

    def pkcs7_unpad(self, s):
        """
        unpadding according to PKCS #7
        @param s: string to unpad
        @type s: byte
        @rtype: byte
        """
        sd = -(s[-1])
        return s[0:sd]

    def encrypt(self, plain_text):
        if (plain_text is None) or (len(plain_text) == 0):
            raise ValueError('input text cannot be null or empty set')

        plain_bytes = plain_text.encode('utf-8')
        # plain_bytes = plain_text

        if self.pad_mode == self.PKCS5_PAD:
            raw = self.pkcs5_pad(plain_bytes)
        else:
            raw = self.pkcs7_pad(plain_bytes)

        # if isinstance(raw, str):
        #     raw = raw.encode()

        cipher = AES.new(self.secret_key, self.aes_mode, self.iv)
        cipher_bytes = cipher.encrypt(raw)

        return cipher_bytes

    def do_encrypt(self, plain_text):
        return self.base64_encode(self.encrypt(plain_text))

    def decrypt(self, cipher_data):
        if isinstance(cipher_data, str):
            cipher_bytes = cipher_data.encode('utf-8')
        else:
            cipher_bytes = cipher_data

        cipher = AES.new(self.secret_key, self.aes_mode, self.iv)
        plain_pad = cipher.decrypt(cipher_bytes)

        if self.pad_mode == self.PKCS5_PAD:
            plain_text = self.pkcs5_unpad(plain_pad)
        else:
            plain_text = self.pkcs7_unpad(plain_pad)

        return plain_text.decode()

    def do_decrypt(self, cipher_data):
        return self.decrypt(self.base64_decode(cipher_data))

    def base64_encode(self, bytes_data):
        """
        加base64

        :type bytes_data: byte
        :rtype 返回类型: string
        """
        return (base64.urlsafe_b64encode(bytes_data)).decode()

    def base64_decode(self, str_data):
        """
        解base64

        :type str_data: string
        :rtype 返回类型: byte
        """
        return base64.urlsafe_b64decode(str_data)


if __name__ == '__main__':
    iv = b'\x9b+\x16U\xabZ\xfb\x91\x0bLd\xa7\xd9\x05\xde]'
    secret_key = '@packer.password'
    plain_text = 'packer.hello'

    encrypted_data = AESCrypt(secret_key, iv).do_encrypt(plain_text)
    print(encrypted_data)

    decrypted_data = AESCrypt(secret_key, iv).do_decrypt(encrypted_data)
    print(decrypted_data)
