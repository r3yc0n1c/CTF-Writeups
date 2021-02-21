from Crypto.Cipher import ARC4
import os

KEY = os.urandom(16)
FLAG = "darkCON{RC4_1s_w34k_1f_y0u_us3_s4m3_k3y_tw1c3!!}"

menu = """
+--------- MENU ---------+
|                        |
| [1] Show FLAG          |
| [2] Encrypt Something  |
| [3] Exit               |
|                        |
+------------------------+
"""

print(menu)

while 1:
	choice = input("\n[?] Enter your choice: ")

	if choice == '1':
		cipher = ARC4.new(KEY)
		enc = cipher.encrypt(FLAG.encode()).hex()
		print(f"\n[+] Encrypted FLAG: {enc}")

	elif choice == '2':
		plaintext = input("\n[*] Enter Plaintext: ")
		cipher = ARC4.new(KEY)
		ciphertext = cipher.encrypt(plaintext.encode()).hex()
		print(f"[+] Your Ciphertext: {ciphertext}")

	else:
		print("\n:( See ya later!")
		exit(0)
