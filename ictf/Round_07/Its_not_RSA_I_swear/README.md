## It's not RSA, I swear!

> I spiced up my not-RSA with randomness! They told me it's secure, so you won't be able <br>
> to retrieve my super duper secret message... Right? (Thanks to A~Z (Aztro) for this challenge!) <br>
> Attachments <br>
> :arrow_down: [File](chall.zip) <br>
> Category <br>
> Crypto <br>
> Points <br>
> 175

## Solution
The Encryption part has some **Linear Congruential Generators(LCG)** stuffs going on as,

<p align="center"><b>
nonce = (a * nonce + b) % m
</b></p>

and the flag being encrypted in a fancy way by using **modular inverse** of the **nonce** with respect to the modulus **n**.

```py
def you_thought_it_was_rsa_encryption_but_it_was_me_dio(data, n, e):
	m = randrange(n)
	a = randrange(m)
	b = randrange(m)
	nonce = randrange(m)

	for d in data.hex():
		yield pow(e, int(d, 16), n) * pow(nonce, -1, n) % n
		nonce = (a*nonce + b) % m   # kinda LCG stuffs
```

The first approach is to find the nonces using the **known plaintext = ictf{** which gives us first **10** hex nibbles of the flag and 
with these we can recover the corresponding nonces like this,

<p align="center"><b>
c = pow(e, d, n) * pow(nonce, -1, n) % n <br>
nonce = inv_mod( c * inv_mod( pow(e, d), n ) , n)
</b></p>

Then crack the LCG to get the parameters and further predict/generate all the nonces like [this](https://tailcall.net/blog/cracking-randomness-lcgs/),

<p align="center"><b>
  a - The Multiplier <br>
  b - The Increment <br>
  m - The Modulus
</b></p>

```py
"""
LCG Cracker
"""
def get_inc(states, m, n):
	s1 = states[0]
	s2 = states[1]
	return ( s2 - m * s1) % n

def get_mult(states, n):
	s1 = states[0]
	s2 = states[1]
	s3 = states[2]
	m = ((s3 - s2) * inverse(s2-s1, n)) % n
	return m

def get_mod(states):
	diffs = [b - a for a, b in zip(states, states[1:])]
	z = [a*c - b**2 for a, b, c in zip(diffs, diffs[1:], diffs[2:])]
	n = reduce(GCD, z)
	return n

m = get_mod(nonce) 
a = get_mult(nonce, m)
b = get_inc(nonce, a, m) 
```
Now we just need to brute-force all the hex digits ( [0-9a-f] ) and get the flag.

```py
def crack(m, a, b, nonce, enc_flag):
	flag = ''	
	hexchars = '0123456789abcdef'
	for c in enc_flag:
		nonce = (a*nonce + b) % m
		for d in hexchars:
			if pow(e, int(d, 16), n) * pow(nonce, -1, n) % n == c:
				flag += d
	return flag
```

Full Solution Script - [apex.py](apex.py)

## Flag
> ictf{d0n'7_us3_b4d_n0nc3s_k1d5}
