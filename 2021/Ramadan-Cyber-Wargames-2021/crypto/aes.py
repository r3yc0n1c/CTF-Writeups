from Crypto.Cipher import AES

import hashlib
import socketserver
import random
import binascii

from Crypto.Util.Padding import pad, unpad

KEY = b''
FLAG = "CTFAE{}"
menu = """
1. encrypt(plaintext)
2. decrypt(ciphertext)
"""


def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)
    if plaintext.decode() == "log in as admin to get the flag1337":
        return "dont play smart"
    if len(plaintext) % 16 != 0:
        return "error: Data length must be multiple of 16"
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(plaintext)
    return "ciphertext:" + encrypted.hex()


def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)
    if len(ciphertext) % 16 != 0:
        return "error: Data length must be multiple of 16"
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    try:
        decrypted = unpad(decrypted, 16).decode()
    except ValueError:
        decrypted = decrypted.decode()
        return decrypted
    if decrypted == "log in as admin to get the flag1337":
        return FLAG


def handle(self):
    self.send(menu)
    try:
        enterd = int(self.read())
    except ValueError:
        self.send("ERROR: Please select a menu option")

    if enterd not in [1, 2]:
        self.send("ERROR: Please select a menu option")

    if enterd == 1:
        self.send("enter plaintext in hex to encrypt:")
        plaintext = self.read()

        if plaintext == "":
            self.send("you entered empty plaintext")
        else:
            ct = encrypt(plaintext)
            self.send(ct)

    if enterd == 2:
        self.send("enter ciphertext in hex to decrypt:")
        ciphertext = self.read()
        if ciphertext != "":
            pln = decrypt(ciphertext)
            self.send(pln)
        else:
            self.send("you entered empty ciphertext")


class RequestHandler(socketserver.BaseRequestHandler):
    handle = handle

    def read(self, until='\n'):
        out = ''
        while not out.endswith(until):
            out += self.request.recv(1).decode()
        return out[:-len(until)]

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")
        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def close(self):
        self.request.close()


class Server(socketserver.ForkingTCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        self.request.close()






