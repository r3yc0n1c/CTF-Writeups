from Crypto.Util.number import *
# from sage.all import *

flagEU = 848630917051893087050233654298398605870572417880786546004017
# print(flagEU.bit_length())
# flag = long_to_bytes(flagEU)
# print(flag)
# print(len(flag))
# print(flag.hex())

n_orig = 943005855809379805541572246085636463198876208104363395594609
e = 65537

def test_neg_msg():
	n = getPrime(96)*getPrime(96)
	print('n:', n)
	c = pow(-1,e,n)
	print('c:',c)

	assert n-1 == c

def find_N_m1():
	"""
	We have E(x) = x**65537 - k*n, for some integer k (which will be 
	different for different values of x), and the unknown modulus n, 
	and hence x**65537 - E(x) will always be a multiple of n.

	So, compute: gcd(2**65537 - E(2), 3**65537 - E(3))

	That will be n multiplied by some integer which is likely to be small...
	"""
	pt1, ct1 = (2,405518048190558088634310202493589629933137815074909354184258)
	pt2, ct2 = (3,736006545906739541375355456172047521086543171458483024077845)
	
	for k in range(2, 2**16):
		n = GCD(pow(pt1,e) - ct1, pow(pt2,e) - ct2) // k
		print(f"[+] Gusseing N [k={k}]: {n}")
		if n == n_orig:
			print("SUCCESS!!!")
			break

def find_N_m2():
	"""
	As similar method (that doesn't involve computing on such large 
	integers, and even works even if you don't know e) is to compute:

	gcd(E(2)2 - E(4),E(3)2−E(9))

	How this works should be fairly obvious...
	"""

	pt1, ct1 = (2,405518048190558088634310202493589629933137815074909354184258)
	pt2, ct2 = (3,736006545906739541375355456172047521086543171458483024077845)
	pt3, ct3 = (4,28287358476740482187432197716177875720480221862681611755228)
	pt4, ct4 = (9,767583012794049034673272177772960869366486503190863559274779)

	for k in range(2, 2**16):
		n = GCD(ct1**2 - ct3, ct2**2 - ct4) // k
		print(f"[+] Gusseing N [k={k}]: {n}")
		if n == n_orig:
			print("SUCCESS!!!")
			break

def find_N_m3():
	pt1, ct1 = (2,405518048190558088634310202493589629933137815074909354184258)
	pt2, ct2 = (3,736006545906739541375355456172047521086543171458483024077845)
	pt3, ct3 = (4,28287358476740482187432197716177875720480221862681611755228)
	pt4, ct4 = (5,118164290266571816954914720950212104095415618051341152315626)

	n_x = GCD(pow(pt1,e) - ct1, pow(pt2,e) - ct2)
	n_y = GCD(pow(pt4,e) - ct4, pow(pt3,e) - ct3)

	n = GCD(n_x, n_y)
	print(n)


# find_N_m1()
# find_N_m2()
find_N_m3()

