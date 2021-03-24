from mt19937predictor import MT19937Predictor
from pwn import *

r = remote('challs.dvc.tf', 3096)
predictor = MT19937Predictor()


print(r.recvuntil("Let's play a game. If you can tell me what number I am thinking of, I will give you the flag."))

log.progress("Collectiong states...")

for i in range(624):
	if i % 50 == 0:
		print(f" [\t{i}\t]")
	r.recvuntil("What number am I thinking of? ")
	r.sendline("0")		# Send wrong guess
	s = int( r.recvline().decode().split()[-1] )
	# print(len(states))
	# states.append(int(s[-1]))
	predictor.setrandbits(s, 32)

print("===== DONE =====")

pred = predictor.getrandbits(32)
print(f"Predicted: {pred}")

r.sendline(str(pred))
r.interactive()

# dvCTF{tw1st3d_numb3rs}