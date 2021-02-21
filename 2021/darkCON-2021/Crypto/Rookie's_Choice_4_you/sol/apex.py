#!/usr/bin/env python3
from Crypto.Cipher import ARC4

FLAG = '385e95136bdb2a66baa0593e27b8df03228f1785ea9925c768d08b74b06bffe27bd17da1aed51c21342026bdacb173f8'
FLAG = bytes.fromhex(FLAG)

pl = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
enc_pl = '3d5d841c4df203758189060d7ba5ef0460c90faeae890dc621dfb563a03cc5f728d42794ae8a08102f2766acece427f3c6514fc7'
enc_pl = bytes.fromhex(enc_pl)

cx = [a ^ b for a,b in zip(FLAG, enc_pl)]
pl = [ord(i) for i in pl]

rec = ''.join( [chr(i ^ j) for i,j in zip(pl,cx)] )
print(rec)
