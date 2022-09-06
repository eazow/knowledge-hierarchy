# -*- coding:utf-8 -*-
import os
import socket
import argparse

SERVER_ADDRESS = "10.91.3.37", 8888
REQUEST = """
GET /hello HTTP/1.1
Host: 10.91.3.37:8888
"""


def send_requests(max_clients, max_conns):
    socks = []
    for client_num in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for connection_num in range(max_conns):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(SERVER_ADDRESS)
                sock.sendall(REQUEST)
                socks.append(sock)
                os.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="test client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--max-conns",
        type=int,
        default=1024,
        help="Maximum number of connections per client"
    )
    parser.add_argument(
        "--max-clients",
        type=int,
        default=1,
        help="Maximum number of clients"
    )
    args = parser.parse_args()
    send_requests(args.max_clients, args.max_conns)