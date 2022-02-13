import jwt
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('secret', metavar='secret', type=str, nargs='?',
                        default='secret', help='the secret key to encode the jwt (default %(default)s)')
    parser.add_argument('payload', metavar='payload', type=str, nargs='?',
                        default='{"some": "payload"}', help='the json object to encode (default %(default)s)')
    return parser.parse_args()


def main():
    args = parse_args()
    encoded_jwt = jwt.encode(json.loads(args.payload),
                             args.secret, algorithm="HS256")
    print(encoded_jwt)


if __name__ == "__main__":
    main()
