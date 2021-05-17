#!/usr/bin/env python3
from Crypto.Util.Padding import pad
import binascii
from pprint import pprint

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

ivs = []
def decrypt(blocks, pad):	
	for b in blocks:
		d = byte_xor(binascii.unhexlify(b), pad)
		# print(d)
		if d not in ivs:
			ivs.append(d)

pad = b'}' + b'\x0f'*15		# guess flag's last char }
# print(pad)
file = open('data.txt').read().strip().split('\n')
for c, data in enumerate(file):
	blocks = eval(data)
	# print(blocks)
	# print('-'*50 + '[' + str(c+1) + ']')
	decrypt(blocks, pad)

print("\n[+] GOT encrypted IV s...\n")
pprint(ivs)
print("\n[+] Bruteforcing...")

for c, data in enumerate(file):
	blocks = eval(data)			# every 96 byte enc data div into chunks 32
	# print(blocks)
	print('-'*50 + '[ SAMPLE ' + str(c+1) + ']')
	for b in blocks:
		for iv in ivs:
			d = byte_xor(binascii.unhexlify(b), iv)
			print(d)

# flag{I_7h0ught_7h1s_wa5_@_s3cr3t}
