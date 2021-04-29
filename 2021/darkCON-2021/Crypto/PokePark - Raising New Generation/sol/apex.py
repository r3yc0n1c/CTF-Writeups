from Crypto.Util.number import inverse, GCD
from functools import reduce

def get_inc(states, m, n):
	s1 = states[0]
	s2 = states[1]
	return ( s2 - m * s1) % n

def get_mult(states, n):
	s1 = states[0]
	s2 = states[1]
	s3 = states[2]
	m = ((s3 - s2) * inverse(s2-s1, n)) % n
	return m

def get_mod(states):
	diffs = [b - a for a, b in zip(states, states[1:])]
	z = [a*c - b**2 for a, b, c in zip(diffs, diffs[1:], diffs[2:])]
	n = reduce(GCD, z)
	return n

def predict_state(curr_state, n, m, c):
	pred = (m * curr_state + c) % n
	return pred

if __name__ == '__main__':

	states = [1997095401, 13001997, 1628715232, 1990339562, 284249215, 1372925577, 48385624, 1468364002, 2059193937, 26044107]

	n = get_mod(states)
	print("n:", n)

	m = get_mult(states, n)
	print("m:", m)

	c = get_inc(states, m, n)
	print("c:", c)

	print("predicted:", predict_state(states[-1], n, m, c))
