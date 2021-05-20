# Basic (100)
> INKEMQKFPNRGC4ZRMNZV6YLSMVPWC3DXIB4XGX3OGFRWKIL5

## Solution
The ciphertext looks like all-caps some encoding so the first thing that comes to mind is `base32` and there we find the flag.

https://gchq.github.io/CyberChef/#recipe=From_Base32('A-Z2-7%3D',false)&input=SU5LRU1RS0ZQTlJHQzRaUk1OWlY2WUxTTVZQV0MzRFhJQjRYR1gzT0dGUldLSUw1

## Flag
> CTFAE{bas1cs_are_alw@ys_n1ce!}

***

# Polynomial (100)
> Polynomials talks, what does it say? <br>
> Flag format : CTFAE{whatever_the_polynomial_says} <br>
> :arrow_down: [polynomial.txt](polynomial.txt)

## Solution
What we have is a simple polynomial which gives us the flag after converting it to the `Integer` form.

The `python3` version:
```py
#!/usr/bin/env python3

def f(x):
	return x**62+x**61+x**59+x**58+x**54+x**53+x**48+x**46+x**45+x**44+x**42+x**40+x**38+x**37+x**34+x**33+x**32+x**30+x**29+x**27+x**22+x**21+x**19+x**16+x**14+x**13+x**11+x**10+x**9+x**6+x**5+x**2+x+1

m = f(2)
flag = "CTFAE{" + bytes.fromhex(hex(m)[2:]).decode() + "}"
print(flag)
```
OR the `sage` version:
```py
#!/usr/bin/env sage

P = PolynomialRing(GF(2),'x')
poly = P(x**62+x**61+x**59+x**58+x**54+x**53+x**48+x**46+x**45+x**44+x**42+x**40+x**38+x**37+x**34+x**33+x**32+x**30+x**29+x**27+x**22+x**21+x**19+x**16+x**14+x**13+x**11+x**10+x**9+x**6+x**5+x**2+x+1)
m = ZZ(list(poly), base=2)
flag = "CTFAE{" + bytes.fromhex(hex(m)[2:]).decode() + "}"
print(flag)
```

## Flag
> CTFAE{laughing}

***

# OTP (271)
> Play fast. Connect to the challenge at crypto.ctf.ae:1340.

> :arrow_down: [OTP.py](OTP.py)

## Solution
Looking at the script, we can see the `generate_key()` function creates the key from the **hash of current time** and this is our attack vector. 

```py
def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()

```
We can match the time and thus we'll have the same key as the server. Then we can simply XOR the ciphertext to get the flag.

### Solve Script: [otp_crack.py](otp_crack.py)
```py
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
```

## Flag
> CTFAE{Run_Barry_Run}

***

# AES (676)
> Can you be an admin? Connect to the challenge at crypto.ctf.ae:1401 <br>
> :arrow_down: [aes.py](aes.py)

## Solutions
So we have an `AES-ECB Oracle` in this challenge which lets us encrypt or decrypt anything.

A little bit of info about `AES-ECB` here,

![ecb-enc](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/ECB_encryption.svg/902px-ECB_encryption.svg.png)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/ECB_decryption.svg/902px-ECB_decryption.svg.png)

As you can see, unlike the `CBC` mode, the blocks in `AES-ECB` are encrypted individually and decryption also follows the same process.

Our main goal is to make the plaintext equal to 

`"log in as admin to get the flag1337"`

after decryption but the Oracle doesn't let us encrypt this perticular text as a whole. So, the other way around is to break the plaintext into chunks and encrypt them individually and then join  the ciphertext blocks so that the oracle decrypts them correctly and it matches our target plaintext.

### Solve Script: [aes_hack.py](aes_hack.py)
```py
from Crypto.Util.Padding import pad
from pwn import *

context.log_level = "DEBUG"

p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

""" MENU
1. encrypt(plaintext)
2. decrypt(ciphertext)
"""

msg = b"log in as admin to get the flag1337"
msg = pad(msg, 16)

chunk1 = msg[:32].hex()
chunk2 = msg[32:].hex()

# send chunk1
p.sendline('1')
p.recvuntil('enter plaintext in hex to encrypt:\n')
p.sendline(chunk1)

chipher1 = p.recvline().decode().strip().split(':')[1]

p.close()
p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

# send chunk2
p.sendline('1')
p.recvuntil('enter plaintext in hex to encrypt:\n')
p.sendline(chunk2)

chipher2 = p.recvline().decode().strip().split(':')[1]

p.close()
p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

# join 2 chunks to fool ECB
payload = chipher1 + chipher2
p.sendline('2')
p.recvuntil('enter ciphertext in hex to decrypt:\n')
p.sendline(payload)

p.interactive()

```
## Flag
> CTFAE{cut_and_paste_is_freakYy}

***

# Random (775)
> Randomness!? <br>
> :arrow_down: [Random.zip](Random.zip)

## Solution
This is so far the most effortless challenge from a player's perspective! Just calculate the modular multiplicative inverse and the flag is yours!

You will find this helpful -

[Modular multiplicative inverse function in Python](https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)

or use this shortcut - 

`pow(a, -1, b)` (works for python3.8+)

```py
#!/usr/bin/env python3

ct=  12537576051804175563327586976670029631566047287638078998089754690645624344231550445991707158491229698148411522554155816496036779806555485834952506608559
h=  60265484187477817500261541037127766652469415139848324866328181422045589130178011981346418737196705385289671967114630965939110799802899878375479313346670
f= 2370571969473031684637173230550879122895526230953301488944136519211944736476441195070705438364020785212931399972537

m = ct * pow(f,-1,h) % h
print(bytes.fromhex(hex(m)[2:]))

```
## Flag
> CTFAE{multiplicative_invers_is_nice}

***

# modpower (964)
> Some data was leaked, is it important? <br>
> :arrow_down: [modpower.zip](modpower.zip)

## Solution
This challenge actually touches different domains and lets you choose the attack vector carefully. So, let's divide it for better understanding.

### The Encryption
```py
def encrypt(m,par1,par2,l):
 for i in range(0,l):
  cipher.append((ord(m[i])^(par1[i]^par2[i])))
 return cipher
```
The ecnryption is based on XOR of 3 different parts which tells us that the only way to recover the plaintext is to find the 2 random parts and XOR them again.

Let's move on to the next part.

### The Random Number Generation (par1)
```py
import random

# [...snip...]

for i in range(25,1000):
   par1.append((random.getrandbits(32)))
   # [...snip...]

# [...snip...]
```
This is Python's default random number generation module and this - 

[https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html)

tells us about the default algorithm that Python uses to generate those random numbers.

The next thing is how do we crack this ???
Luckily someone made a python implementation of the cracker here -

[https://github.com/kmyk/mersenne-twister-predictor](https://github.com/kmyk/mersenne-twister-predictor)

Now, let's move on to the next part.

### The n-th power residue calculation (par2)
```py
# [...snip...]

for i in range(25,1000):
   # [...snip...]
   par2.append(pow(x,i,p))

# [...snip...]
```
Here, `par2` contains the `n-th power residues` of `x` ( which is a 8 bit integer <sup>[1]</sup> ) modulo `p` ( which is a 50 bit prime <sup>[1]</sup> ).

With some quick maths, we can see that,

Let's say, <br>
<p align='center'>
s1 = par2[0] = x^25 mod p <br>
s2 = par2[1] = x^26 mod p <br>
s3 = par2[2] = x^27 mod p <br><br>
s2 = (s1 * x) mod p <br>
s3 = (s2 * x) mod p
</p>

You might have got this! Yes this acts like a [Linear Congruential Generator](https://en.wikipedia.org/wiki/Linear_congruential_generator) ( more precisely, it's like the [Lehmer random number generator](https://en.wikipedia.org/wiki/Lehmer_random_number_generator) version )

and here - 

[Cracking a linear congruential generator](https://security.stackexchange.com/questions/4268/cracking-a-linear-congruential-generator)

we can find a nice explaination with the math behind it to crack this thing.

But we need some `states` to find `x and p` and recover whole `par2`. We have the cipher array and the flag starts with `CTFAE{`.

Now,
```
cipher[i] = ord(m[i]) ^ par1[i] ^ par2[i]
par2[i] = ord(m[i]) ^ par1[i] ^ cipher[i]
```
So, we can recover the first 6 numbers/states in `par2` by this method and 6 states are enough to recover the  rest of it.

Now, we're all set to implement the whole thing...

> [1] That I later got to know after cracking the RNG

### Solve Script: [sol.py](sol.py)
```py
from mt19937predictor import MT19937Predictor
from sympy.ntheory.modular import crt
from Crypto.Util.number import *
import gmpy2


def encrypt(m,par1,par2,l):
	c = []
	for i in range(0,l):
		c.append((ord(m[i])^(par1[i]^par2[i])))
	return c


leaked= [...snip...]
cipher= [...snip...]

predictor = MT19937Predictor()

for i in range(624):
	predictor.setrandbits(leaked[i], 32)

# assert predictor.getrandbits(32) == part1[624]

npart1 = leaked + [predictor.getrandbits(32) for _ in range(975-624)]

# assert npart1 == part1

npart1 = npart1[::-1]
known = 'CTFAE{'
npart2 = encrypt(known,npart1,cipher,len(known))
print(npart2)

"""
LCG(lehmar) Cracker implementation here from this script - https://github.com/r3yc0n1c/CTF-Writeups/blob/main/2021/darkCON-2021/Crypto/PokePark%20-%20Raising%20New%20Generation/sol/apex.py

c0 = x**25 % p
c1 = x**26 % p = c0*x % p
c2 = x**27 % p = c1*x % p
"""
p = 584086853872567
x = 220

# assert [pow(x,i,p) for i in range(25,25+6)] == npart2

par2 = []

for i in range(25,1000):
   par2.append(pow(x,i,p))

flag = [a^b^c for a,b,c in zip(cipher,npart1,par2)]
flag = ''.join([chr(i) for i in flag])
print(flag)


```
## Flag
> CTFAE{9ae1c1434b676e5ddbc3874a9e6e46ff05e39eff}
