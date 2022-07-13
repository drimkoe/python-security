from hashlib import sha256
from cryptography.fernet import Fernet
import hmac
import zlib
import json
import os

class Cryptography:

    def __init__(self,data : bytes):
        self.data = data
        self.symmetric_key = Fernet.generate_key()

    def get_digest(self):
        hash_function = sha256(self.data)
        return hash_function.digest()

    def get_checksum(self):
        return zlib.crc32(self.data)

    def get_message_auth_code(self):
        key = os.urandom(16)
        hmac_sha256 = hmac.new(key, self.data,sha256)
        return hmac_sha256.digest()

    def hmac_equals(self, other):
        return hmac.compare_digest(self.get_message_auth_code(), other.get_message_auth_code())

    def get_symmetric_token(self):
        cipher = Fernet(self.symmetric_key)
        return cipher.encrypt(self.data)

    def deciper(self,message : bytes):
        cipher = Fernet(self.symmetric_key)
        return cipher.decrypt(message)
