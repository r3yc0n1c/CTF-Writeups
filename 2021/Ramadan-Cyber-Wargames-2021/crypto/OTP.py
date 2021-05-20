import string
import binascii
import hashlib
import socketserver
import random
import time
from Crypto.Util.number import long_to_bytes

menu = """
1. encrypt
2. flag
"""


def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()


def encrypt(b):
    key = generate_key()
    assert len(b) <= len(key)
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i]])
    return ciphertext.hex()


def handle(self):
    FLAG = b'CTFAE{}'
    self.send(menu)
    try:
        enterd = int(self.read())

    except ValueError:
        self.send("ERROR: Please select a menu option")

    if enterd not in [1, 2]:
        self.send("ERROR: Please select a menu option")

    if enterd == 1:
        self.send("enter plaintext in hex to encrypt:")
        plaintext = bytes.fromhex(self.read())
        if plaintext != "":
            ct = encrypt(plaintext)
            self.send(ct)
        else:
            self.send("you entered empty plaintext")
    if enterd == 2:
        self.send("encrypted flag:")
        ct = encrypt(FLAG)
        self.send(ct)


class RequestHandler(socketserver.BaseRequestHandler):
    handle = handle

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")
        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def read(self, until='\n'):
        out = ''
        while not out.endswith(until):
            out += self.request.recv(1).decode()
        return out[:-len(until)]

    def close(self):
        self.request.close()


class Server(socketserver.ForkingTCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        self.request.close()













