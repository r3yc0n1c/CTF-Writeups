#!/usr/bin/env python3
# https://www.w3schools.com/python/ref_random_seed.asp
import random

data = open('flag.enc', 'rb').read()

# find seed
chunk = data[-18:]		# 18 coz time.time() returns 18 digits number
seed = []
for i in chunk:
	seed.append(i ^ 0x99)	 # the last 18 bytes are XORed against the same byte - 0x99
print(seed)

ct = ''.join(chr(i) for i in seed)
print(ct)		# the time when the flag was encoded

# If you use the same seed value twice you will get the same random number twice.
# set seed
random.seed(ct)

flag = data[:len(data)-18]
# generate the same random number used by the user to encrypt
k1 = [random.randrange(256) for _ in flag]		
print(k1)

dec = bytearray()
for m,k in zip(data, k1 + [0x99]*len(ct)):
	dec.append(m^k)

print(dec.decode())
