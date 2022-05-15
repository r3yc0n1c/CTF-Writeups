flag = list(open("encrypted_flag.txt", "r").read())
l = len(flag)
# print(l)

for i in range(l):
    flag[i]=chr(ord(flag[i])>>1)

for i in range(1,l+1,2):
    for j in range(i):
        flag[j]= chr(ord(flag[j])^42)

for i in range(0,l+1,2):
    for j in range(i):
        flag[j]=chr(ord(flag[j])^1337)

# print(flag)
print(''.join(flag))

# zionctf{ju5t_7he_r3gul4r_x0r_s7uff_yeetyeet}
