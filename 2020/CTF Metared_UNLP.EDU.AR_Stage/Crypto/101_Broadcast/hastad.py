#!/usr/bin/env python3

"""
Author:       	r3yc0n1c
Date:         	26 November 2020 (Thursday)
Description:  	Hastad's Broadcast Attack for RSA
				https://en.wikipedia.org/wiki/Coppersmith's_attack#H.C3.A5stad.27s_broadcast_attack
Requirements:	pip3 install sympy gmpy2
"""
from sympy.ntheory.modular import crt
import gmpy2
import sympy

def get_flag(n):
	print(f"{'='*30} D E C O D E D {'='*30}\n")
	print(bytes.fromhex(hex(n)[2:]))
	print()

def main():
	file = open('reto3').read().strip().split('\n')
	
	n = []
	c = []
	for line in file:
		if 'n' in line:
			n.append(int(line.split(':')[1]))
		else:
			c.append(int(line.split(':')[1]))

	e = 3
	
	# RSA Hastad's Attack
	M = crt(n, c)[0]
	print(f"[+] CRT Result:\n{M}\n")
	msg = gmpy2.iroot(M,e)[0]
	print(f"[+] ith root :\n{msg}\n")
	
	get_flag(msg)

if __name__ == "__main__":
	main()