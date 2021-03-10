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
	p = process('./debug.rb')

	p.recvuntil("> ")	# prompt

	rounds = 10
	p.sendline(str(rounds))

	data = p.recvuntil("And finally...").decode().strip().split('\n')

	cheat = data[0]
	log.success(f"{cheat} [{len(data)}]")

	data = data[8: -2]

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

	# DEBUG MODE
	cheat = cheat.split()[-1]
	cheat_idx = WORDS.index(cheat)
	idx = predictor.getrandbits(32) & 0xFFFF
	w = WORDS[idx]

	print(f"orig word: {cheat} [{cheat_idx}]")
	print(f"word pred: {w} [{idx}]")
	
	# p.interactive()

if __name__ == '__main__':
	main()