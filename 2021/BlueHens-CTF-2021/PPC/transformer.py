from pwn import *

p = remote("challenges.ctfd.io", 30008)

# TODO: run the script again and again

for i in range(100):
	print( p.recvline().decode() )
	p.recvline()
	task = p.recvuntil("@@@@@")
	print(task)

	todo, data = task.split(b": ")
	data = data[:-6]
	# print(todo, data)

	lol = ''

	if todo == b'convert hexdigest to integer':
		lol = int(data.decode(), 16)
		p.sendline(str(lol))

	elif todo == b'convert hexdigest to string':
		lol = bytes.fromhex(data.decode())
		# lol = "".join(map(chr, data))
		p.sendline(lol)

	elif todo == b'convert hexdigest to bytearray':
		lol = list(bytes.fromhex(data.decode()))
		p.sendline(str(lol))

	elif todo == b'convert bytearray to string':
		data = eval(data)
		lol = bytes(data)
		p.sendline(lol)

	elif todo == b'convert bytearray to hexdigest':
		data = eval(data)
		lol = bytes(data).hex()
		p.sendline(lol)

	elif todo == b'convert bytearray to integer':
		data = eval(data)
		lol = int.from_bytes(data, 'big')
		p.sendline(str(lol))

	elif todo == b'convert string to bytearray':
		lol = list(data)
		p.sendline(str(lol))

	elif todo == b'convert string to hexdigest':
		lol = data.hex()
		p.sendline(lol)

	elif todo == b'convert string to integer':
		lol = int.from_bytes(data, 'big')
		p.sendline(str(lol))

	elif todo == b'convert integer to bytearray':
		n = int(data.decode())
		lol = n.to_bytes((n.bit_length() + 7) // 8, 'big')
		lol = list(lol)
		p.sendline(str(lol))

	elif todo == b'convert integer to hexdigest':
		lol = hex(int(data.decode()))[2:]
		p.sendline(lol)

	elif todo == b'convert integer to string':
		n = int(data.decode())
		lol = n.to_bytes((n.bit_length() + 7) // 8, 'big')
		p.sendline(lol)

	print(f"[ans]> {lol}")

	p.recvline()
	print(p.recvline().decode())		# propmt
	p.recvline()


p.interactive()


# UDCTF{r0b075_1N_d15gu153}
