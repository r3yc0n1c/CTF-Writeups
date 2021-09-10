#!/usr/bin/env python3
from Crypto.Cipher import AES
from functools import reduce
import hashlib, string, sys
from tqdm import tqdm

'''
python3 solve.py <start-index>
'''


def xor(*inputs):
    return bytes(reduce(lambda x, y: x ^ y, i) for i in zip(*inputs))

def pad(message):
    padding = bytes((key_len - len(message) % key_len) * chr(key_len - len(message) % key_len), encoding='utf-8')
    return message + padding

def blocksplit(data, n):
	return [data[i:i+n] for i in range(0,len(data),n)]	

def decrypt(key, last_block):	
	hidden = hashlib.sha256(key).digest()[:10]
	message = b'CBC (Cipher Blocker Chaining) is an advanced form of block cipher encryption' + hidden
	msg = pad(message)
	pt_blocks = blocksplit(msg, 16)	
	rec_out = last_block

	for ptb in reversed(pt_blocks[1:]):
		ecb = AES.new(key, AES.MODE_ECB)
		dec_raw = ecb.decrypt(last_block)
		curr_block = xor(ptb, dec_raw)
		rec_out = curr_block + rec_out
		last_block = curr_block

	res = rec_out.hex()
	if all(out[i] == res[i] for i in range(len(out)) if out[i] != '*'):
		rec_iv = xor(AES.new(key, AES.MODE_ECB).decrypt(rec_out[:16]), msg[:16])
		print(f'{key = }')
		print(f'{res = }')
		print(f'{rec_iv = }')


key = b'*XhN2*8d%8Slp3*v'
key_len = len(key)
out = '9**********b4381646*****01********************8b9***0485******************************0**ab3a*cc5e**********18a********5383e7f**************1b3*******9f43fd66341f3ef3fab2bbfc838b9ef71867c3bcbb'
last_block = bytes.fromhex(out[-32:])

# Limit brute combos to 10 chars at a time
idx = int(sys.argv[1])
alpha = string.printable[idx:idx+10]

for a in tqdm(alpha):
	for b in tqdm(string.printable):
		for c in string.printable:
			key = f'{a}XhN2{b}8d%8Slp3{c}v'.encode('latin-1')
			decrypt(key, last_block)


# TMUCTF{Y0U_D3CrYP73D_17}
