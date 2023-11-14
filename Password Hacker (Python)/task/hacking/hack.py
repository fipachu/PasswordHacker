import dataclasses
import itertools as it
import socket
import argparse
import string


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
    alphabet = string.ascii_lowercase + string.digits

    for i in it.count(start=1):
        passwords = it.product(alphabet, repeat=i)
        passwords = (''.join(p) for p in passwords)
        yield from passwords


def brute_force(client):
    for candidate in get_passwords():
        client.send(candidate.encode())
        response = client.recv(1024).decode()

        match response:
            case 'Connection success!':
                print(candidate)
                break
            case 'Too many attempts.' as s:
                print(f'Error! Server response: {s}')
                break


def main():
    config = Config()

    with socket.socket() as client:
        client.connect(config.address)

        brute_force(client)


if __name__ == "__main__":
    main()
