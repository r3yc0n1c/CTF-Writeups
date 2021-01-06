# AES ECB (388)
> Strong crypto doesn't always meet strong expectations. <br>
> `nc chall.bsidesalgiers.com 5002`

## Sol
ECB Byte at a Time Attack

- [x] Mode Detection - **ECB** (from the chall desc)
- [x] Block size detection -
- Send input until length of ciphertext changes. 
- **Blocksize** = **length of new ciphertext(no. of bytes)** - **length of old ciphertext(no. of bytes)**

```py
from pwn import *
import base64
import string

# nc chall.bsidesalgiers.com 5002
r = remote('chall.bsidesalgiers.com', 5002)
pt = ""
blocksize = 16

def enc(s):    
    r.sendline(s)
    r.recvuntil(': ')
    data = r.recvline().decode().strip()
    dec = base64.b64decode(data).hex()
    return dec 

if __name__ == '__main__':
	pl = 'A'*15
	key = ''

	""" TEST
	r.recvuntil(': ')
	got = enc(pl)
	c1 = got[:32]
	print(got)
	print(c1)

	for i in range(ord('!'),ord('~')+1):
		# r.recvuntil(': ')
		got = enc(pl + chr(i))
		c2 = got[:32]
		print(i)
		if c1==c2:
			print(chr(i), i)
			break
	"""
	
	alphs = string.printable
	for k in range(10):
		b = ""
		for i in range(1,17):
			pl = "A"*(16-i)
			# r.recvuntil(': ')
			r.recv()

			g1 = enc(pl)
			g1 = g1[:32+k*32]
			print("String sent: ",pl)

			# for j in range(ord('!'),ord('~')+1):
			for j in alphs:
				# print(j)
				g2 = enc(pl+pt+b+j)
				g2 = g2[:32+k*32]
				if g1 == g2 and ord(j)!=10 and ord(j)!=0:
					print(ord(j), j)
					b += j
					if j=="}":
						print(pt+j,end="")
						exit()
					break
			# print("LAGGED!!!")
		pt += b
		print(pt)
```

## Flag
> **shellmates{I_though_AES_w4s_m1l1tary_gr4de_encryp7ion_1n_al1_m0des}**

## Ref
* [CSAW Quals 2017 - BabyCrypt](https://amritabi0s.wordpress.com/2017/09/18/csaw-quals-2017-babycrypt-writeup/)
