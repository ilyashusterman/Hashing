import argparse
import hashlib
import hmac
import json
import logging
import base64


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', help='Simulate, do not create AppNexus objects', action='store_true')
    args = parser.parse_args()
    hash_key = hmac.new('1234'.encode(),
                        'ilyailyua'.encode(),
                        hashlib.sha256)
    key = hash_key.hexdigest()
    # print(hmac.compare_digest(key))
    print(json.dumps({'key': key}, indent=2))
    print(base64.b64decode(key, ))
    base64.b64encode(key.encode()).decode()
    dig = hmac.new(b'1234567890', msg=your_bytes_string,
                   digestmod=hashlib.sha256).digest()
    base64.b64encode(dig).decode()  # py3k-mode
    'Nace+U3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg='

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
