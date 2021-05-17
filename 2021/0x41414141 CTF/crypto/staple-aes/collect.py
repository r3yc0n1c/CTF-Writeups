#!/usr/bin/env python3
from pwn import *

context.log_level = 'ERROR'

def collect(size):
	file = open('data.txt', 'w')

	# nc 185.172.165.118 3167 		# US
	# nc 161.97.176.150 3167		# EU
	for i in range(size):
		# r = remote('185.172.165.118', 3167)		# US
		r = remote('161.97.176.150', 3167)		# EU
		print(f"[+] Got # {i+1}")
		data = r.recv().decode().strip()
		s = ', '.join( ['\''+data[i:i+32]+'\'' for i in range(0,len(data),32)] )
		# print(s)
		file.write('[' + s + ']\n')
	file.close()

if __name__ == '__main__':		
	size = 3		# no of unique enc data we want
	
	collect(size)

	while 1:
		file = open('data.txt')
		rem = set(file.read().strip().split('\n'))
		file.close()
		if len(rem) < size:
			print("Unique Samples:", len(rem))
			file = open('data.txt', 'w').write('\n'.join(rem))			
			collect(size)
		else:
			print(f"DONE!!! Collected {size} samples")
			break
