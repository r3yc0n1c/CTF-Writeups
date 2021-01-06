import itertools as it
import string
import hashlib

target = '2bafea54caf6f8d718be0f234793a9be'

alphs = string.ascii_lowercase
combos = it.permutations(alphs, 5)

print("[+] Starting Bruteforce...")
for c in combos:
	passwd = ''.join(c) + '04532@#!!'
	hashed = hashlib.md5(passwd.encode()).hexdigest()
	# print(passwd, hashed)
	if hashed == target:
		print("[+] Passwd:", passwd)
		break

# Found! passwd: brute04532@#!!
# Flag: brute
