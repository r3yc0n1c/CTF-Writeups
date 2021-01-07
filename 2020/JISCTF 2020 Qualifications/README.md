# # Baby Crypto (200)
> :arrow_down:  [baby.zip](baby.zip)

## Solution
```py
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

```
## Flag
> **JISCTF{B4BY_ENCRYPT10N_JISCTF2020_QUALIFICATION_RND_101}**

# # N0T-B4By (300)
> :arrow_down:  [not_baby.zip](not_baby.zip)

## Solution
```py
file = open("flag.enc").read().strip()

k = []
# print(file)
for i in range(0,len(file),32):
	try:
		a = int(file[i:i+32])
		b = int(file[i+32:i+64])
		# print(a, b, a^b)
		k.append(a^b)
	except:
		pass

kp = ord('J')
print(k)
# exit()
f = 'J'
for i in range(len(k)):
	f += chr(k[i]^kp)
	kp = k[i]^kp

print(f)
```
## Flag
> **JISCTF{R4ND0M_NUMB3RS_4S_K3Y_!!!}**
