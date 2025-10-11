# -*- coding: utf-8 -*-

from polaris_crypto.aes_cipher import AESCipher


if __name__ == '__main__':
    key = "6789045129812345"
    cipher = AESCipher(key)
    message = "Hello, World!"
    encrypted_message = cipher.encrypt(message)
    print("Encrypted:", encrypted_message)
    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted:", decrypted_message)