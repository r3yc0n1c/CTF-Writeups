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


def get_n(pairs):
	pt1, ct1 = pairs[0]
	pt2, ct2 = pairs[1]
	pt3, ct3 = pairs[2]
	pt4, ct4 = pairs[3]

	n_x = GCD(pow(pt1,e) - ct1, pow(pt2,e) - ct2)
	n_y = GCD(pow(pt4,e) - ct4, pow(pt3,e) - ct3)

	n = GCD(n_x, n_y)
	
	return n


flagEU = 848630917051893087050233654298398605870572417880786546004017
flagUS = 248460643464675800653780615843208617730874812788255456931910
# print(flag.bit_length())
# flag = long_to_bytes(flag)
# print(flag, len(flag))

print("\n[+] Finding N from (plaintext, ciphertext) pairs...\n")

e = 65537			# std guess e

pl = [2,3,4,5]
pairs = []
for i in pl:
	r.recvline()
	r.sendline(str(i))
	enc = int(r.recvline()[2:-1].decode())
	pairs.append( (i, enc) )
	print(f"({i},{enc})")

n = get_n(pairs)
print(f"\nFound N: {n}")

# n = 943005855809379805541572246085636463198876208104363395594609

p,q = [882152190529044698706991746907,1068983182191997868299760689187]
phi = (p-1)*(q-1)
d = inverse(e,phi)
pt = pow(flagEU,d,n)
flag = long_to_bytes(pt)
print(f"\n[+] Flag: {flag}")

# y0u_d0nt_n33d_4nyth1ng