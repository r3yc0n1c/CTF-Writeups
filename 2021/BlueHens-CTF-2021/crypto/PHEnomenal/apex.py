from pwn import *

# nc challenges.ctfd.io 30004 
p = remote("challenges.ctfd.io", 30004)

# Given E(m) and n^2, we can find E(am) = pow(Em, a, n^2)

p.recvline()
p.recvline()

c1 = int(p.recvline().split()[-1])
print(c1)

p.recvline()

m1 = int(p.recvline().split()[-2])
print(m1)

p.recvline()

n_2 = int(p.recvline().split()[-1])
print(n_2)

p.recvline()
m2 = p.recvuntil("? ").split()[-1]
m2 = int(m2[:-1])
print(m2)

a = m2//m1
c2 = pow(c1,a,n_2)
print(c2)

p.sendline(str(c2))
p.interactive()

# UDCTF{P41ll13R_one_oh_one}
