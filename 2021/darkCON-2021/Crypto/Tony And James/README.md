# Tony And James Writeup (45 solves / 472 points)

### Source Script
```py
#!/usr/bin/env python3
import random

# custom seed generation
def get_seed(l):
	seed = 0
	rand = random.getrandbits(l)
	raw = list()
	
	while rand > 0:
		rand = rand >> 1
		seed += rand
		raw.append(rand)
	
	if len(raw) == l:
		return raw, seed
	else:
		return get_seed(l)

def encrypt(m):
	l = len(m)

	raw, seed = get_seed(l)		# get raw_state and seed
	random.seed(seed)

	with open('encrypted.txt', 'w') as f:
		# char by char encoding of the FLAG
		for i in range(l):
			r = random.randint(1, 2**512)
			if i == 0:
				print("r0 =",r)     # the 1st random number (r0) that we have
			encoded = hex(r ^ m[i] ^ raw[i])[2:]
			f.write(f"F{i}:  {encoded}\n")

def main():
	m = open('flag.txt').read()
	encrypt(m.encode())			# Encrypt the FLAG

if __name__=='__main__':
	main()
```

The leakage of 1st generated random number makes the encryption vulnerable because we already know the flag format.

So we can use the leaked random number and the **Known Plaintext Attack** on the **XOR Encryption** to obtain the **seed**.

After generating the seed, we can set the seed and we will obtain the same random numbers that were used in the encryption 

([same seed produces same random numbers](https://stackoverflow.com/questions/22639587/random-seed-what-does-it-do#answer-22639752))
and then decrypt the flag.

### Solve Script
```py
import random

def get_seed(raw_00, l):
	seed = 0
	raw = [raw_00]
	for i in range(1,l):
		seed += raw_00
		raw.append(raw_00 >> 1)
		raw_00 = raw_00 >> 1
	return raw, seed

def decrypt(file, r0):
	"""
	By Properties of XOR,

	encoded[i] = r ^ m[i] ^ raw[i]
	raw[i] = r ^ m[i] ^ encoded[i]

	For i = 0 we know,
	m[0] = 'd'  ( because flag format is darkCON{} )
	r = r0
	encoded[0] = first encoded hex (F0)
	"""
	# Calculate start of seed
	raw_00 = r0 ^ ord('d') ^ int(file[0].split(': ')[1], 16)
	l = len(file)
	raw, seed = get_seed(raw_00, l)
	random.seed(seed)

	flag = ''
	for i in range(l):
		x = int(file[i].split(':  ')[1], 16)
		r = random.randint(1, 2**512)
		flag += chr(x ^ raw[i] ^ r)
	print(flag)


file = open('encrypted.txt').read().strip().split('\n')
r0 = 13006113194937977865329550196847254275750805445133166331150790640161443707848964445638439062364681023973459358767889599334590592762861309365461149844507558
decrypt(file, r0)
```

## Flag
darkCON{user_W4rm4ch1ne68_pass_W4RM4CH1N3R0X_t0ny_h4cked_4g41n!}
