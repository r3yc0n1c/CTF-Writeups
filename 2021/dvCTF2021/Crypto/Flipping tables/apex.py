from pwn import *
import string

# nc challs.dvc.tf 3333
r = remote('challs.dvc.tf', 3333)
alphs = string.printable

def get_block(s):
	while True:
		r.sendline(s)
		enc = r.recvline().split()
		if b'!E(input' in enc:
			continue
		return enc[-1]

def main():
	flag = ''

	for n in range(10):
		h = ''
		for i in range(1, 17):
			pl1 = b'A'*(16-i)
			pl1 = pl1.hex()

			r.recvuntil('What do you want me to encrypt? ')

			b1 = get_block(pl1)
			b1 = b1[:32 + n*32]

			for char in alphs:
				char = char.encode().hex()
				pl2 = pl1 + flag + h + char
				b2 = get_block(pl2)
				b2 = b2[:32 + n*32]
				print(f"pl1: {pl1} | b1: {b1} | pl2: {pl2} | b2: {b2}")
				if b1 == b2:
					print("FOUND: {} -> {}".format(char, bytes.fromhex(char).decode()))
					h += char
					if char == hex(ord('}'))[2:]:
						print(bytes.fromhex(flag + h).decode())
						exit()
					break
		flag += h
		print("[BLOCK{}]: {}".format(n, bytes.fromhex(flag).decode()))

def test():
	PAYLOAD = '00'*15	# 15 bytes
	r.recvuntil('What do you want me to encrypt? ')
	flag = ''

	enc = get_block(PAYLOAD)[:32]
	
	print(enc)

	for char in alphs:
		h = hex(ord(char))[2:]
		PAYLOAD = '00'*15 + h
		found = get_block(PAYLOAD)[:32]

		print(f"p: {PAYLOAD} | enc: {enc} | found: {found}")
		if enc == found:
			print(f"GOT!!!: {char}")
			flag += char
			break


if __name__ == '__main__':
	# test()
	main()

# dvCTF{3CB_4ngry_0r4cl3}
