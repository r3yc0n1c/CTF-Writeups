# https://maojui.me/Writeups/0ctf/2019/babyrsa/

from public_key import e,n
from sage.all import GF, PolynomialRing
from Crypto.Util.number import long_to_bytes, bytes_to_long

enc = open('secret','rb').read().strip().split(b'\n\n\n')

R.<a> = GF(2^2049)
P = PolynomialRing(GF(2),'x')
n = P(n)

p,q = n.factor()
p,q = p[0],q[0]
np = pow(2, p.degree())
nq = pow(2, q.degree())
phi = (np-1) * (nq-1)
d = inverse_mod(e, phi)

pt = b''

for c in enc:
	c_idx_int = bytes_to_long(c)
	c_idx_poly = P(R.fetch_int(c_idx_int))
	idx_poly = pow(c_idx_poly,d,n)
	idx_int = R(idx_poly).integer_representation()
	pt += long_to_bytes(idx_int)

print(pt)
