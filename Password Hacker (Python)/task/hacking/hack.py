import dataclasses
import socket
import argparse


@dataclasses.dataclass(slots=True)
class Config:
    address: tuple[str, int]
    message: bytes


def config() -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port', type=int)
    parser.add_argument('message')
    args = parser.parse_args()

    return Config(
        (args.ip, args.port),
        args.message.encode()
    )


def main():
    con = config()

    with socket.socket() as client:
        client.connect(con.address)
        client.send(con.message)
        response = client.recv(1024).decode()

        print(response)


if __name__ == "__main__":
    main()
