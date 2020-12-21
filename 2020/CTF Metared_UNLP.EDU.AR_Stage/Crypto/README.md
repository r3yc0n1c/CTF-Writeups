#  Rsa Warmup (50)
> nc rsa.ctf.cert.unlp.edu.ar 5003

## Solution
### Solve Script: [rsa.py](rsa.py)
```py
from pwn import *
import gmpy2
from Crypto.Util.number import long_to_bytes as l2b

def get_it():
	return int(r.recvline().strip().decode().split(' ')[1])

def solve_rsa(p, q, e, c):
	n = p*q
	phi = (p-1) * (q-1)
	d = gmpy2.invert(e, phi)
	m = l2b(pow(c,d,n))
	return m

# nc rsa.ctf.cert.unlp.edu.ar 5003
r = remote("rsa.ctf.cert.unlp.edu.ar", 5003)
r.recv()
r.recvline()
r.recvline()
r.recvline()

p = get_it()
q = get_it()
e = get_it()
c = get_it()

m = solve_rsa(p,q,e,c)
print(f"Decoded:\n{m}")

r.sendline(m)

r.interactive()
```
## Flag
> flag{rsa_is_eeeeeeasy}
