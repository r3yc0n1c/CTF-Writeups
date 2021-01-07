from Crypto.Util.number import isPrime, GCD, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def decrypt(ciphertext, privkey):
	cipher = PKCS1_OAEP.new(privkey)
	m = cipher.decrypt(ciphertext)	
	print(m)

def get_d(p, q, e):
	phi = (p-1)*(q-1)
	key = inverse(e, phi)
	return key

def main():
	print("[+] Decoding the Comms...")

	alice_pubkey = RSA.importKey(open('alice_public.pem').read())	# Importing Alice's Public key
	n1 = alice_pubkey.n
	e1 = alice_pubkey.e

	bob_pubkey = RSA.importKey(open('bob_public.pem').read())	# Importing Bob's Public key
	n2 = bob_pubkey.n
	e2 = bob_pubkey.e

	# Common Factor (Prime) Attack

	x = GCD(n1, n2)

	p1 = x
	q1 = n1//p1

	assert isPrime(p1) == 1
	assert isPrime(q1) == 1
	assert p1*q1 == n1

	p2 = x
	q2 = n2//p2

	assert isPrime(p2) == 1
	assert isPrime(q2) == 1
	assert p2*q2 == n2

	alice_d = get_d(p1, q1, e1)
	bob_d = get_d(p2, q2, e2)

	# Alice decrypts Bob's msg with Alice's Private key
	alice_privkey = RSA.construct((n1, e1, alice_d))		# Retriving Alice's Private key
	ciphertext = open('bob_message.oaep', 'rb').read()
	print("\n[+] Bob's msg...\n")
	decrypt(ciphertext, alice_privkey)

	# Bob decrypts Alice's msg with Bob's Private key
	bob_privkey = RSA.construct((n2, e2, bob_d))			# Retriving Bob's Private key
	ciphertext = open('alice_message.oaep', 'rb').read()
	print("\n[+] Alices's msg...\n")
	decrypt(ciphertext, bob_privkey)

if __name__ == '__main__':
	main()