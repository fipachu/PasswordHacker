import dataclasses
import socket
import argparse


@dataclasses.dataclass(slots=True)
class Config:
    address: tuple[str, int]
    message: bytes

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('ip')
        parser.add_argument('port', type=int)
        parser.add_argument('message')
        args = parser.parse_args()

        self.address = args.ip, args.port
        self.message = args.message.encode()


def main():
    config = Config()

    with socket.socket() as client:
        client.connect(config.address)
        client.send(config.message)
        response = client.recv(1024).decode()

        print(response)


if __name__ == "__main__":
    main()
