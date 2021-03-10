#!/usr/bin/env python3
from mt19937predictor import MT19937Predictor
from pwn import *

FIRST_NAMES = open('first-names.txt').read().strip().split('\n')
LAST_NAMES  = open('last-names.txt').read().strip().split('\n')
WORDS       = open('words.txt').read().strip().split('\n')

predictor = MT19937Predictor()

def get_nums(players):
	p1, p2 = players.split(' -vs- ')
	p1 = p1.strip()
	p2 = p2.strip()

	p1_first, p1_last = p1.split()
	p2_first, p2_last = p2.split()

	LSB = FIRST_NAMES.index(p1_first)
	MSB = LAST_NAMES.index(p1_last)
	N1 = (MSB << 16) | LSB

	LSB = FIRST_NAMES.index(p2_first)
	MSB = LAST_NAMES.index(p2_last)
	N2 = (MSB << 16) | LSB

	assert FIRST_NAMES[N1 & 0xFFFF] == p1_first
	assert LAST_NAMES[N1 >> 16] == p1_last
	assert FIRST_NAMES[N2 & 0xFFFF] == p2_first
	assert LAST_NAMES[N2 >> 16] == p2_last

	return N1, N2


def main():
	# p = process('./hangman.rb')
	# nc -v hangman-battle-royale-2d147e0d.challenges.bsidessf.net 2121
	p = remote("hangman-battle-royale-2d147e0d.challenges.bsidessf.net", 2121)

	p.recvuntil("> ")	# prompt

	# we need 2^10 sates to feed first 624 to the cracker
	rounds = 10
	p.sendline(str(rounds))

	data = p.recvuntil("And finally...").decode().strip().split('\n')
	data = data[6: -2]
	# print(data)


	for i, players in enumerate(data):
		n1, n2 = get_nums(players)
		# print(n1, n2, sep='\n')
		if i < 624//2:
			predictor.setrandbits(n1, 32)
			predictor.setrandbits(n2, 32)
		else:
			p1 = predictor.getrandbits(32)
			p2 = predictor.getrandbits(32)

			assert p1 == n1 and p2 == n2
			# print(f"n1: {n1} | n2: {n2}")
			# print(f"p1: {p1} | p2: {p2}")
			# sleep(1)

	predictor.getrandbits(32)	# waste

	pred_words = []

	for i in range(rounds, 0, -1):

		idx = predictor.getrandbits(32) & 0xFFFF	# weird sample() in ruby
		word = WORDS[idx]
		# log.success(f"ROUND {10-i+1} : {word}")
		pred_words.append(word)

		# waste predictor
		for _ in range(1, ((2**i) >> 1)):
			predictor.getrandbits(64)

	# Send Predicted words
	for i, w in enumerate(pred_words):
		p.recvuntil("Your guess --> ")
		log.progress(f"ROUND {i+1} : {w}")
		p.sendline(w)
		# sys.stdout.write(p.recvuntil("Press enter to continue").decode())
		print(p.recvuntil("Press enter to continue").decode())
		p.sendline('\n')	# push to next round
		# p.interactive()
		p.recvuntil("Press enter to continue")
		p.sendline('\n')	# push to next round

	p.interactive()


if __name__ == '__main__':
	main()


"""
Press enter to continue
$ 
You win this round!
Wow, that was a MEGA victory!
Flag: CTF{hooray_mt19937}
"""