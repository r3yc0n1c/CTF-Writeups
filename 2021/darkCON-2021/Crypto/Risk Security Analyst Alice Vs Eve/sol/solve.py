from Crypto.Util.number import *
from collections import namedtuple

Publickey = namedtuple("Publickey", ['n','e'])

# End To End RSA Decryption
def E2ERD(pubkey, phi):
    enc_chats = open('encrypted_chats.txt').read().strip().split('\n\n')
    pubs = open('all_publickeys.txt').read().strip().split('\n\n')

    for i, chat in enumerate(enc_chats):
        user, msg = chat.split(': ')
        e, n = eval(pubs[i].split(': ')[1])
        c = bytes_to_long(eval(msg))
        d = inverse(e, phi)
        m = long_to_bytes(pow(c,d,n)).decode()
        print(f"{user}: {m}")

def predict_phi(n, e, d):
    k = ((e*d) - 1)//n
    while 1:
        phi = ((e*d) - 1)//k
        if phi*k == ((e*d) - 1):
            return phi
        k += 1

def main():
    n= 134871459832923860099882590902411996710996766501756653086495354300954191050110475349218593219906710987168729946490859346117437393705213066464123381634516073655104369957424501917959364716066521838138728063315157921217685558557422845878448233922585713677077217815414960315913375048754314176130997193108410703707
    e= 65537
    d= 19546349779408743507159083393977587389734764914989772052665408473846268620686776856842366882870347146743497520969378855752070133900119225861364479282918556646891456167647366904804199245738822376442388779257291859758735359459148377679538927373263135165396852614400167982261412234666697210259242937381901648593
    pubkey = Publickey(n, e)
    
    pphi = predict_phi(n,e,d)
    E2ERD(pubkey, pphi)

if __name__ == '__main__':
    main()
