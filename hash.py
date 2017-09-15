import argparse
import hashlib
import hmac
import json
import logging
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',
                        help='Simulate, do not create AppNexus objects',
                        action='store_true')
    args = parser.parse_args()
    # encrypt_only()
    # set password
    password = 'mysecretpassword'
    # set message
    message = 'secretmessage'
    salt = 'static_salt'
    encrypt = generate(message, password, salt=salt,
                           action='encrypt')
    decrypt = generate(encrypt, password, salt='static_salt', action='decrypt')
    output_encryption = {
        'message': message,
        'password': password,
        'salt': salt,
        'key': encrypt.decode(),
        'decoded_message': decrypt.decode()
                         }
    print(json.dumps(output_encryption, indent=2))


def encrypt_only():
    hash_key = hmac.new('1234'.encode(),
                        'ilyailyua'.encode(),
                        hashlib.sha256)
    key = hash_key.hexdigest()
    # print(hmac.compare_digest(key))
    print(json.dumps({'key': key}, indent=2))


def generate(message, password, salt, action):
    message = message.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt.encode(),
                     iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    if action == 'encrypt':
        encrypted = f.encrypt(message)
        answer = {'key': encrypted.decode()}
        return answer
    elif action == 'decrypt':
        decrypted = f.decrypt(message)
        answer = {'message': decrypted.decode()}
        return answer


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
