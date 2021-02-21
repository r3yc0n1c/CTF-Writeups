# Rookie's_Choice_4_you (51 solves / 467 points)
> :arrow_down: [Chall File](dist/dist.zip)

### [Source Script](src/src.py)
```py
#!/usr/bin/env python3
from Crypto.Cipher import ARC4	# pip3 install pycryptodome
import os

KEY = os.urandom(16)
FLAG = "******************* REDUCTED *******************"

menu = """
+--------- MENU ---------+
|                        |
| [1] Show FLAG          |
| [2] Encrypt Something  |
| [3] Exit               |
|                        |
+------------------------+
"""

print(menu)

while 1:
	choice = input("\n[?] Enter your choice: ")

	if choice == '1':
		cipher = ARC4.new(KEY)    # Key for RC4
		enc = cipher.encrypt(FLAG.encode()).hex()
		print(f"\n[+] Encrypted FLAG: {enc}")

	elif choice == '2':
		plaintext = input("\n[*] Enter Plaintext: ")
		cipher = ARC4.new(KEY)    # Same key is reused
		ciphertext = cipher.encrypt(plaintext.encode()).hex()
		print(f"[+] Your Ciphertext: {ciphertext}")

	else:
		print("\n:( See ya later!")
		exit(0)
```
## The Attack
It was the **Reused Key Attack** on RC4 Stream Cipher. Let **RC4(A)** be the Encryption function and **K** be the Key. 
RC4 produces a string of bits KSA(K) (say KS) the same length as the messages where KSA is the Function implementing the Key-scheduling algorithm

<p align="center">
RC4(m1) = m1 ⊕ KS = c1 <br>
RC4(m2) = m2 ⊕ KS = c2 <br><br>
And by the <a href="https://en.wikipedia.org/wiki/Exclusive_or#Properties"> Properties of XOR </a> we can calculate <br><br>
c1 ⊕ c2 = (m1 ⊕ KS) ⊕ (m2 ⊕ KS) = m1 ⊕ m2 ⊕ KS ⊕ KS = m1 ⊕ m2
</p>

Now say **m1** was the **FLAG** and **m2** was our known plaintext. So, we can recover FLAG by
<p align="center">
m1 = (m1 ⊕ m2) ⊕ m2
</p>

### [Solve Script](sol/apex.py)
```py
from Crypto.Cipher import ARC4

FLAG = '385e95136bdb2a66baa0593e27b8df03228f1785ea9925c768d08b74b06bffe27bd17da1aed51c21342026bdacb173f8'
FLAG = bytes.fromhex(FLAG)

pl = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
enc_pl = '3d5d841c4df203758189060d7ba5ef0460c90faeae890dc621dfb563a03cc5f728d42794ae8a08102f2766acece427f3c6514fc7'
enc_pl = bytes.fromhex(enc_pl)

cx = [a ^ b for a,b in zip(FLAG, enc_pl)]
pl = [ord(i) for i in pl]

rec = ''.join( [chr(i ^ j) for i,j in zip(pl,cx)] )
print(rec)
```

## Flag
> darkCON{RC4_1s_w34k_1f_y0u_us3_s4m3_k3y_tw1c3!!}

## Ref
* [RC4 - Wiki](https://en.wikipedia.org/wiki/RC4)
* [Stream cipher attacks - Wiki](https://en.wikipedia.org/wiki/Stream_cipher_attacks)
