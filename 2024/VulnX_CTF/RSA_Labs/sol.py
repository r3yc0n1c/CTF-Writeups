from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from math import isqrt
import tqdm


def is_square(a):
    if a <= 0:
        return False
    return a == isqrt(a) ** 2


# modified fermat
# https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
# a = p +- 2^k-1 + x/2     b = +- 2^k-1 + x/2


def factorize(n, r):
    p, q = 0, 0
    for x in range(-(10**4), +(10**4)):
        b = 2 ** (r - 2) + x
        if is_square(b**2 + n):
            p = isqrt(n + b**2) + b
            break
        if is_square(b**2 - n):
            p = isqrt(b**2 - n) + b
            break
        b += 1

    if p:
        q = n // p
    return p, q


key = RSA.import_key(open("pub.pem").read())
n, e = key.n, key.e

pbits = n.bit_length() // 2
print(n)
print(e)
print(pbits)

for r in tqdm.trange(pbits, 2, -1):
    p, q = factorize(n, r)
    if p:
        print(f"{r = }")
        print(p, q)
        break

phi = (p-1)*(q-1)
assert GCD(e, phi) == 1

c = bytes_to_long(open("flag.txt.enc", "rb").read())
d = inverse(e, phi)
m = pow(c, d, n)
flag = long_to_bytes(m)
print(flag)
