import socket
import os
import threading


class NameServer:
    def __init__(self, config: dict):
        self.server_thread = threading.Thread(target=server_loop,
                                              args=[config, self])
        self.server_thread.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((config["ns"]["ip"], config["ns"]["port"]))


def server_loop(config, name_server: NameServer):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((config["ns"]["ip"], config["ns"]["port"]))

    while True:
        message, address = server_socket.recvfrom(1024)
