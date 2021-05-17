#!/usr/bin/env python3
from pwn import *

# nc 45.134.3.200 9660
r = remote('45.134.3.200', 9660)

def towerOfHanoi():
	print("Tower of Hanoi")
	
	for i in range(25):		# from testing got 25 problems
		data = eval(r.recvline().decode().strip())
		# print(data)
		m = pow(2, len(data)) - 1		
		print(f"[ {i} ] \t [moves]>", m)
		r.recv() 	# recv '>'
		r.sendline(str(m))
		i+=1

def getInvCount(arr, n): 
  
    inv_count = 0
    for i in range(n): 
        for j in range(i + 1, n): 
            if (arr[i] > arr[j]): 
                inv_count += 1
    return inv_count

def merge_sort():
	print("Merge Sort inversions count")

	for i in range(25):		# from testing got 25 problems
		data = eval(r.recvline().decode().strip())
		# print(data)
		m = getInvCount(data, len(data))
		print(f"[ {i} ] \t [inv count]>", m)
		r.recv() 	# recv '>'
		r.sendline(str(m))
		i+=1
	
  
def main():
	print(r.recvline())		# prompt
	print(r.recvline())		# prompt
	
	towerOfHanoi()

	print(r.recvline())		# prompt
	
	merge_sort()

	r.interactive()

if __name__ == '__main__':
	main()

# you won here's your flag flag{g077a_0pt1m1ze_3m_@ll}
