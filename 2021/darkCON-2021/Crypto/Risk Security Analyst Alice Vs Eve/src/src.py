from Crypto.Util.number import *
from collections import namedtuple
import random

Publickey = namedtuple("Publickey", ['n','e'])
Privatekey = namedtuple("Privatekey", ['n','e','d','p','q'])

def get_key_pair(bits):
    p = getStrongPrime(bits)
    q = getStrongPrime(bits)
    n = p*q
    e = 65537
    phi = (p-1)*(q-1)
    d = inverse(e, phi)
    return Publickey(n, e), Privatekey(n, e, d, p, q)
    
def gen_public_exps(size, privkey):
    phi = (privkey.p - 1)*(privkey.q - 1)
    exps = []
    c = 0
    while c < size:
        k = random.randrange(10, 20)
        e = pow(4, k) + 1
        if e not in exps and GCD(e, phi)==1:
            exps.append(e)
            c += 1
    return exps

# End To End RSA Encryption
def E2ERE(users, data, pubkey, privkey):
    
    phi = (privkey.p - 1)*(privkey.q - 1)
    exps = [pubkey.e] + gen_public_exps(users, privkey)

    alice_secret = 'n: ' + str(pubkey.n) + '\ne: ' + str(pubkey.e) + '\nd: ' + str(privkey.d)
    with open('alice_secret.txt', 'w') as f:
        f.write(alice_secret)

    enc_chats = open('encrypted_chats.txt', 'w')
    pubs = open('all_publickeys.txt', 'w')

    for i in range(users):
        user, msg = data[i].split(' : ')
        m = bytes_to_long(msg.encode())
        c = pow(m, exps[i], pubkey.n)
        encrypted = long_to_bytes(c)
        enc_chats.write(user + ': ' + str(encrypted) + '\n\n')
        pubs.write(user + ': (' + str(exps[i]) + ',' + str(pubkey.n) + ')\n\n')

def main():
    bits = 512
    users = 5

    print(f"[+] [ users: {users} ]")
    
    pubkey, privkey = get_key_pair(bits)
    
    print('-'*30)
    print(f"[+] Generated Keys !!!")

    data = open('chats.txt').readlines()
    E2ERE(users, data, pubkey, privkey)

    print("[+] Encryption Successfull")

if __name__ == '__main__':
    main()
