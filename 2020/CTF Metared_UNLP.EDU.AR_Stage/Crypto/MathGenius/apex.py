import sympy
from pwn import *

""" ref
https://medium.com/@cxzero/owasp-latam-at-home-ctf-2020-write-up-81485800afcc
"""

def con():
	# nc mathgenius.ctf.cert.unlp.edu.ar 5002
	r = remote("mathgenius.ctf.cert.unlp.edu.ar", 5002)
	try:		
		# scrape nums
		r.recvuntil('[')
		tmp = r.recv().strip()[:-1]
		data = tmp.split(b',')
		nums = []
		for n in data:
			nums.append(int(n.decode()))
		return nums
	except:
		r.interactive()


ri = list()
for i in range(10):	
	print(f"[*] Collecting Sample No. [ {i} ] ", end='')	
	nums = con()
	ri.append(nums)

print(f"\n[*] Collected Samples:")
with open('nums.txt','w') as f:
	for i in ri:
		f.write(str(i) + '\n')
		print(i)

# Attack
print(f"\n[*] Attacking Rands...")
res=''
for s in range(0,40):
	res +=	chr ( sympy.igcd(ri[0][s] , ri[1][s] , ri[2][s], ri[3][s], ri[4][s], ri[5][s], ri[6][s], ri[7][s], ri[8][s], ri[9][s]) )
print (res)