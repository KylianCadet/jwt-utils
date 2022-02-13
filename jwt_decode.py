import base64
import hashlib
import hmac
import itertools
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('jwt', metavar='jwt', type=str,
                        help='the jwt to decypher')
    parser.add_argument('max', metavar='max', type=int, default=20,
                        nargs='?', help='the max size of the jwt password (default %(default)s)')
    args = parser.parse_args()

    if len(args.jwt.split('.')) != 3:
        print('Bad formatted JWT', file=sys.stderr)
        sys.exit(1)

    header, payload, _signature = args.jwt.split('.')
    try:
        print('Header : ', base64.b64decode(header + "=="))
        print('Payload : ', base64.b64decode(payload + "=="))
    except:
        print('Bad formatted JWT content', file=sys.stderr)
        sys.exit(1)

    return args


def get_password(jwt: str, _max: int) -> bytes:
    header, payload, _signature = jwt.split('.')
    header_and_payload = header + '.' + payload
    header_and_payload_byte = header_and_payload.encode()

    for r in range(1, _max + 1):
        print("Trying with password size : ", r)
        for key in itertools.product(bytes(i for i in range(0, 256)), repeat=r):
            hash_byte = hmac.new(
                bytes(key), header_and_payload_byte, hashlib.sha256).digest()
            hash_b64 = base64.b64encode(hash_byte)
            hash_str = hash_b64.decode('utf-8').replace('/', '_').rstrip('=')
            if hash_str == _signature:
                return bytes(key)
    
    print("Password not found")


def main():
    args = parse_args()
    password = get_password(args.jwt, args.max)
    print(password)


if __name__ == "__main__":
    main()
