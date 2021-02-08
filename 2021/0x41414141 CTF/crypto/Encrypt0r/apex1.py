from Crypto.Util.number import *
from pwn import *

"""
EU instance 161.97.176.150 4449
US instance 185.172.165.118 4449
https://crypto.stackexchange.com/questions/65965/determine-rsa-modulus-from-encryption-oracle
"""
r = remote('161.97.176.150', 4449)
# r = remote('185.172.165.118', 4449)
print(r.recvline()) 	# prompt + enc flag
print(r.recvline()) 	# prompt + enc flag

flagEU = 848630917051893087050233654298398605870572417880786546004017
flagUS = 248460643464675800653780615843208617730874812788255456931910
# print(flag.bit_length())
# flag = long_to_bytes(flag)
# print(flag, len(flag))

pl = -1
r.recvline()
r.sendline(str(pl))
enc = int(r.recvline()[2:-1].decode())
print(f"({pl},{enc})")

n = 943005855809379805541572246085636463198876208104363395594609

assert enc + 1 == n 	# pow(-1, e, n) == n-1

p,q = [882152190529044698706991746907,1068983182191997868299760689187]
phi = (p-1)*(q-1)
e = 65537			# std guess e
d = inverse(e,phi)
pt = pow(flagEU,d,n)
flag = long_to_bytes(pt)
print(flag)

# y0u_d0nt_n33d_4nyth1ng