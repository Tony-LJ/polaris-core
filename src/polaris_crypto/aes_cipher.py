# -*- coding: utf-8 -*-

"""
descr : AES对称加密算法
auther : lj.michale
create_date : 2025/10/10 15:54
file_name : AESCipher.py
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os


class AESCipher:
    def __init__(self, key):
        self.key = key.encode()  # 密钥必须是字节类型
        self.backend = default_backend()

    def _pad(self, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    def _unpad(self, data):
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(data) + unpadder.finalize()

        return unpadded_data

    def encrypt(self, plaintext):
        iv = os.urandom(16)  # 初始化向量
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padded_data = self._pad(plaintext.encode())
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return urlsafe_b64encode(iv + ciphertext).decode()  # 返回base64编码的字符串，便于传输和存储

    def decrypt(self, ciphertext):
        ciphertext = urlsafe_b64decode(ciphertext)
        iv = ciphertext[:16]  # 提取初始化向量
        ciphertext = ciphertext[16:]  # 提取密文数据
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        return self._unpad(decrypted_padded_data).decode()  # 返回解密后的明文


