from Crypto.Util.Padding import pad
from pwn import *

context.log_level = "DEBUG"

p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

""" MENU
1. encrypt(plaintext)
2. decrypt(ciphertext)
"""

msg = b"log in as admin to get the flag1337"
msg = pad(msg, 16)

chunk1 = msg[:32].hex()
chunk2 = msg[32:].hex()

# send chunk1
p.sendline('1')
p.recvuntil('enter plaintext in hex to encrypt:\n')
p.sendline(chunk1)

chipher1 = p.recvline().decode().strip().split(':')[1]

p.close()
p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

# send chunk2
p.sendline('1')
p.recvuntil('enter plaintext in hex to encrypt:\n')
p.sendline(chunk2)

chipher2 = p.recvline().decode().strip().split(':')[1]

p.close()
p = remote("crypto.ctf.ae", 1401)
p.recvuntil('\n\n')

# join 2 chunks to fool ECB
payload = chipher1 + chipher2
p.sendline('2')
p.recvuntil('enter ciphertext in hex to decrypt:\n')
p.sendline(payload)

p.interactive()

# CTFAE{cut_and_paste_is_freakYy}
