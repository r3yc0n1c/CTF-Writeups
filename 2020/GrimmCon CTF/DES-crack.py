from pwn import *

keys = open('keys.txt').read().strip().split('\n')

for k in keys:
	# nc challenge.ctf.games 31692
	r = remote("challenge.ctf.games",  31692)
	r.recv()
	# print(r.recv())
	r.sendline(k)
	
	# try:
	enc = r.recv().decode().strip()[1:]
	dec = bytes.fromhex(enc)
	# print("[+] Encoded: ", enc)
	# print("[+] Decoded: ", dec)

	if b"flag" in dec:
		print("\n[*] Key: ", k)
		print("[*] Decoded: ", dec)
		exit(1)

# [*] Key:  FE1FFE1FFE0EFE0E 
# [*] Decoded:  b'flag{9b9169ac15fe51e8f337bc2786e4fb36}\n\n\n\n\n\n\n\n\n\n'
