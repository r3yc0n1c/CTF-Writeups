# Risk Security Analyst Alice Vs Eve Writeup (21 solves / 488 points)
> La Casa De Tuple (L.C.D.T) is a Company in Spain which provides their own End-to-end encryption services and Alice got a job there.  <br>
> It was her first day and her boss told her to manage the secrets and encrypt the user data with their new End-to-end encryption system. <br>
> You are Eve and you're hired to break into the system. Alice was so overconfident that she gave you everyone's keys. Can you break their <br>
> new encryption system and read the chats? <br>
> :arrow_down: [File](https://github.com/r3yc0n1c/CTF-Writeups/raw/main/2021/darkCON-2021/Crypto/Risk%20Security%20Analyst%20Alice%20Vs%20Eve/dist/dist.zip)

## Solution

As we have the private key of Alice and all the users share the same public modulus, we can easily estimate the **phi** as follows,

```
e * d = 1 mod phi(n)
=> (e*d - 1) is a multiple of phi(n)
=> (e*d - 1) = k*phi(n)
=> k = (e*d - 1)/phi(n) = (e*d - 1)/n 		[ phi(n) = n (approx.) ]

Now, we increase k until phi(n)=(e*d - 1)/k becomes an integer
```

Python code to achive this:
```py
def predict_phi(n, e, d):
    k = ((e*d) - 1)//n
    while 1:
        phi = ((e*d) - 1)//k
        if phi*k == ((e*d) - 1):
            return phi
        k += 1
```

After that we can calaulate everyone's private key,
```
private key of User_i = inverse_mod(e_i, phi(n))
```

And then simple RSA decryption of the encrypted chats will give us the flag.

### [Solve Script](sol/solve.py)
```py
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
```

## Flag
> darkCON{4m_I_n0t_supp0sed_t0_g1v3_d???}

### # Source Code - [[src folder]](src/)
