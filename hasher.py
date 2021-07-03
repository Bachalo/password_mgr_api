import hashlib
import os

class Hasher():

    def hash_password(password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        return salt + key
    
    def verify(input, hashed_password):
        salt_from_hashed_password = hashed_password[:32]
        key_from_hashed_password = hashed_password[32:]

        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            input.encode('utf-8'),
            salt_from_hashed_password,
            100000
        )

        if new_key == key_from_hashed_password:
            return True
        else:
            return False
