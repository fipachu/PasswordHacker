import socket
import argparse


def config() -> tuple[tuple[str, int], bytes]:
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port', type=int)
    parser.add_argument('message')
    args = parser.parse_args()
    return (args.ip, args.port), args.message.encode()


def main():
    address, message = config()

    with socket.socket() as client:
        client.connect(address)
        client.send(message)
        response = client.recv(1024).decode()

        print(response)


if __name__ == "__main__":
    main()
