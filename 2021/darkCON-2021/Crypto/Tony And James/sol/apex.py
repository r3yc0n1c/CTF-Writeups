import random

def get_seed(raw_00, l):
	seed = 0
	raw = [raw_00]
	for i in range(1,l):
		seed += raw_00
		raw.append(raw_00 >> 1)
		raw_00 = raw_00 >> 1
	return raw, seed

def decrypt(file, r0):
	# Calculate start of seed
	raw_00 = r0 ^ ord('d') ^ int(file[0].split(': ')[1], 16)
	# print(start)
	l = len(file)
	raw, seed = get_seed(raw_00, l)
	random.seed(seed)

	flag = ''
	for i in range(l):
		x = int(file[i].split(':  ')[1], 16)
		r = random.randint(1, 2**512)
		flag += chr(x ^ raw[i] ^ r)
	print(flag)


file = open('encrypted.txt').read().strip().split('\n')
r0 = 1251602129774106047963344349716052246200810608622833524786816688818258541877890956410282953590226589114551287285264273581561051261152783001366229253687592
decrypt(file, r0)
