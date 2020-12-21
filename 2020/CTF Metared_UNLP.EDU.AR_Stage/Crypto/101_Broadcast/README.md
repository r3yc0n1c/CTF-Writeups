# 101 Broadcast (250)
> [:arrow_down: rsa101](rsa101) <br>
> Author: @puck

## Solution
Some basic [Hastad's Attack](https://en.wikipedia.org/wiki/Coppersmith's_attack#H.C3.A5stad.27s_broadcast_attack).
### Solve Script: [hastad.py](hastad.py)
```py
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
```
### Output:
```console
root@kali:~/Downloads/certunlp2020/crypto/rsa101# python3 hastad.py 
[+] CRT Result:
27986825396853550819139966548134352016947801394234556764209223278149609974524005782644273850892518172746837949164409494281323229445002199395582642554992275861600104010349845801482643710530503069139523401784011579511906497640759502145431541761125

[+] ith root :
3036112636985152775063347671341292071835224584459595606689986796843345258187019645

============================== D E C O D E D ==============================

b'flag{SYPER_t34m_congr4tulat3s_yoU}'

```
## FLag
> **flag{SYPER_t34m_congr4tulat3s_yoU}**
