import itertools
import hashlib
from pwn import *
import gmpy2

def captcha(target):
	print ('[+] Hacking captcha for', target)
	alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for a,b,c,d,e in itertools.product(alpha, repeat=5):
		X = a+b+c+d+e
		if hashlib.sha256(X.encode()).hexdigest()[-5:] == target:
			return a+b+c+d+e
	print ("[!] Captcha unsolved")
	quit()


""" Low Voltage RSA
https://maxime.puys.name/publications/pdf/PRBL14.pdf
https://eprint.iacr.org/2012/553.pdf
"""
def attack(e,n):
	# Take a shitty message
	m = 7
	# m = hex(m)[2:]

	r.sendline(hex(m)[2:])
	data = r.recv().decode().strip().split('\n\n')
	c = data[0].split(': ')[1]
	# print(data)
	# print(c)
	c = int(c,16)

	p = gmpy2.gcd(pow(c,e,n)-m, n)
	# print(p)
	q = n//p
	if q!=1:					# q == 1 means secure encryption no attack possible
		phi = (p-1)*(q-1)
		d = gmpy2.invert(e,phi)
		return d
	else:
		return 0
		# print(q)
		# print(d)

if __name__ == '__main__':
	# nc challs.xmas.htsp.ro 1006
	r = remote("challs.xmas.htsp.ro", 1006)
	target = r.recv().decode().strip().split(' ')[-1]
	# print(target)
	s = captcha(target).encode().hex()
	r.sendline(s)
	print("[+] Sening POW...")

	data = r.recvuntil('\n\n').decode().strip().split('\n')
	print(data)

	e = int(data[-1].split(':')[1], 16)
	n = int(data[len(data)-2].split(':')[1], 16)
	# print("e: ",e)
	# print("n: ",n)

	print(r.recv().decode())
	for i in range(64):
		print(f"[*] Testing shitty encription {i}")
		option = "1"
		r.sendline(option)
		r.recv()
		d = attack(e,n)
		if d!=0:
			print(f"\n[+] LMAO Noob!!! Your encryption is broken, here is you secret (d) :")
			print(d)
			print()
			break

	# Decrypt with the secret
	r.sendline("2")
	data = r.recv().decode().strip()
	# Get cipher
	ct = data.split(': b\'')[1]
	print(data)
	print(ct)

	ct = int(ct[:-1],16)
	msg = hex(pow(ct,d,n))[2:]

	r.sendline(msg)
	r.interactive()