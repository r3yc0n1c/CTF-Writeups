file = open("flag.enc").read().strip()

k = []
# print(file)
for i in range(0,len(file),32):
	try:
		a = int(file[i:i+32])
		b = int(file[i+32:i+64])
		# print(a, b, a^b)
		k.append(a^b)
	except:
		pass

kp = ord('J')
print(k)
# exit()
f = 'J'
for i in range(len(k)):
	f += chr(k[i]^kp)
	kp = k[i]^kp

print(f)