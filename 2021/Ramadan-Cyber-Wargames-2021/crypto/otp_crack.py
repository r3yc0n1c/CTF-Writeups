from Crypto.Util.number import *
import hashlib, time
from pwn import *

def xor(a, b):
	return bytes(i^j for i,j in zip(a,b))


p = remote("crypto.ctf.ae", 1340)
p.recvuntil("\n\n")
p.sendline("2")
p.recvline()


cipher = p.recvline().decode().strip()
# print(cipher)
cipher = bytes.fromhex(cipher)
known = b"CTFAE{"

current_time = int(time.time()) + 10

for i in range(20):
	t = long_to_bytes(current_time)
	key = hashlib.sha256(t).digest()
	dec = xor(cipher, key)
	if known in dec:
		print(dec, i, current_time)
		break
	current_time -= 1

# CTFAE{Run_Barry_Run}
