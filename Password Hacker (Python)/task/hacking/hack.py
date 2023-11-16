from json import dumps, loads
from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import product
from socket import socket

FILE = (r'C:\Users\filip\OneDrive\PycharmProjects\Password Hacker (Python)'
        r'\logins.txt')
WRONG_LOGIN = {'result': 'Wrong login!'}
WRONG_PASSWORD = {'result': 'Wrong password!'}
BAD_REQUEST = {'result': 'Bad request!'}
EXCEPTION = {'result': 'Exception happened during login'}
SUCCESS = {'result': 'Connection success!'}


@dataclass(slots=True)
class Config:
    address: tuple[str, int]

    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument('ip')
        parser.add_argument('port', type=int)
        args = parser.parse_args()

        self.address = args.ip, args.port


class Credentials(dict):
    def __init__(self, login: str, password: str):
        super().__init__({'login': login, 'password': password})

    def to_json(self, indent=None):
        return dumps(self, indent=indent)


def get_passwords():
    pass


# TODO: check if all case combinations are necessary
#   if they are then why the first two lines of logins.exe??
def get_logins():
    with open(FILE) as f:
        for line in f:
            password = line.strip()

            all_cases = ((c.lower(), c.upper()) if c.isalpha() else (c,)
                         for c in password)
            all_cases = product(*all_cases)
            all_cases = map(''.join, all_cases)

            yield from all_cases


def brute_force_login(client):
    for login in get_logins():
        credentials = Credentials(login, ' ')

        client.send(credentials.to_json().encode())
        response = client.recv(1024).decode()
        response = loads(response)

        # TODO?: match responses as dicts to ignore formatting
        if response == WRONG_PASSWORD:
            return login


def main():
    config = Config()

    with socket() as client:
        client.connect(config.address)

        brute_force(client)
        login = brute_force_login(client)


if __name__ == "__main__":
    main()
