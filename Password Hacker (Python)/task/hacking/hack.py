from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import product
from socket import socket
from sys import stderr

FILE = (r'C:\Users\filip\OneDrive\PycharmProjects\Password Hacker (Python)'
        r'\passwords.txt')


@dataclass(slots=True)
class Config:
    address: tuple[str, int]

    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument('ip')
        parser.add_argument('port', type=int)
        args = parser.parse_args()

        self.address = args.ip, args.port


def get_passwords():
    with open(FILE) as f:
        for line in f:
            password = line.strip()

            all_cases = ((c.lower(), c.upper()) if c.isalpha() else (c,)
                         for c in password)
            all_cases = product(*all_cases)
            all_cases = map(''.join, all_cases)

            yield from all_cases


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

    with socket() as client:
        client.connect(config.address)

        brute_force(client)


if __name__ == "__main__":
    main()
