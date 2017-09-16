import argparse
import hashlib
import hmac
import json
import logging
import base64
from cryptography.fernet import Fernet, InvalidToken
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
    parser.add_argument('--password', default='mysecretpassword',
                        help='Amount of days for optimization')
    parser.add_argument('--phrase', default='static_salt',
                        help='Amount of days for optimization')
    parser.add_argument('--message', default='secretmessage',
                        help='Amount of days for optimization')
    args = parser.parse_args()
    password = args.password
    message = args.message
    salt = args.phrase
    encrypt = generate(message, password, salt=salt,
                       action='encrypt')
    decrypt = generate(encrypt['key'], password, salt='static_salt',
                       action='decrypt')
    output_encryption = {
        'message': message,
        'password': password,
        'salt': salt,
        'key': encrypt,
        'decoded_message': decrypt
    }
    print(json.dumps(output_encryption, indent=2))


def encrypt_only():
    hash_key = hmac.new('1234'.encode(),
                        'ilyailyua'.encode(),
                        hashlib.sha256)
    key = hash_key.hexdigest()
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
        try:
            decrypted = f.decrypt(message)
            answer = {'message': decrypted.decode()}
        except InvalidToken as e:
            answer = {'error': 'invalid key to decrypt '}
        return answer


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
