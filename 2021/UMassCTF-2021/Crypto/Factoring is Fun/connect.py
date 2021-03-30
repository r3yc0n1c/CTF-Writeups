import itertools as it
from pwn import *
import hashlib


def POW(prefix, target):
	charset = string.printable
	for r in range(len(charset)):
		prems = it.product(charset, repeat=r)
		for p in prems:
			dat = prefix + ''.join(p)
			hash = hashlib.sha256(dat.encode()).hexdigest()
			if hash.startswith(target):
				return dat


r = remote("34.69.184.228", 8080)

data = r.recvuntil("> ").split()
prefix = 'UMass-'
target = data[-2].decode()

PoW = POW(prefix, target)
print("PoW = ", PoW)
r.sendline(PoW)

r.interactive()