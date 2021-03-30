# Weird RSA (500)
> Wanna take a look at this challenge? I tried the normal decryption for RSA but for some reason it isn't working. <br>
> [:arrow_down: chall.py](chall.py) <br>
> Created by Soul#8230

## Solution
When I first I looked at the encryption system, it felt odd...wait! It's not RSA at all!!!
After googling some keywords like RSA, recurrence relation cryptosystems, etc. etc. I found this - **"The LUC Cryptosystem"**
and that's it. It's not RSA indeed!

Then I started reading some papers about this Cryptosystem and lucklily I found this 
- [A New Computation Algorithm for a Cryptosystem Based on Lucas Functions](https://thescipub.com/pdf/jcssp.2008.1056.1060.pdf)

which describes LUC very well.


### The Prime Generation
```py
def genPrimes(size):
    base = random.getrandbits(size // 2) << size // 2
    base = base | (1 << 1023) | (1 << 1022) | 1
    while True:
        temp = base | random.getrandbits(size // 4)
        if isPrime(temp):
            p = temp
            break
    while True:
        temp = base | random.getrandbits(size // 4)
        if isPrime(temp):
            q = temp
            break
    return (p, q)

```
At this moment I found that we need to factorize N like in RSA to find the Private Exponent(d) but the Calculation is different. After looking at the `genPrimes()`
function I thought "Oh! these primes are close! yep Fermat will do the work then." and I got the Factors within a couple of secounds. Then I implemented 
the function to calculate **d** from the Paper.

### The Recursion Encryption
```py
def v(n):
    if n == 0:
        return 2
    if n == 1:
        return m
    return (m*v(n-1) - Q*v(n-2)) % N
```
Now, back to the main script where the author used **recursion to implement the encryption** and this works like a trap for us because the recursion limit will
exceed easily for large values of Public Exponent(e).

I was stuck so badly and couldn't figure out how to optimize that. Then I shared my findings with my teammate and he proposed **Memoization** to solve 
this problem, I decided to go through the Paper again and I found the interesting mention of **William's p+1 Algorithm** which I implemented later 
from the wiki itself.

### Solve Script - [solve.sage](solve.sage)
```py
from Crypto.Util.number import *

def fermat_factor(N): 
	if N <= 0: return [N] 
	if is_even(N): return [2,N/2] 
	a = ceil(sqrt(N)) 
	while not is_square(a^2-N): 
	  a = a + 1 
	b = sqrt(a^2-N) 
	return [a - b,a + b]

def legendre(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def get_privatekey(C, p, q, e):
    D = pow(C, 2) - 4    
    LS_p = legendre(D, p)
    LS_q = legendre(D, q)
    
    if LS_p == -1 and LS_q == -1:
        X = p+1
        Y = q+1
    if LS_p == 1 and LS_q == -1:
        X = p-1
        Y = q+1
    if LS_p == -1 and LS_q == 1:
        X = p+1
        Y = q-1
    if LS_p == 1 and LS_q == 1:
        X = p-1
        Y = q-1
    
    R = (X*Y)//GCD(X, Y)	# R = lcm(X, Y)
    d = inverse(e, R)		# e*d mod R = 1
    return d


# Williams's p + 1 algorithm
def LUC(B, a, N):
	x = B
	y = (B**2 - 2) % N
	for bit in bin(a)[3:]:
		if bit == '1':
			x = (x*y - B) % N
			y = (y**2 - 2) % N
		else:
			y = (x*y - B) % N
			x = (x**2 - 2) % N
	return x


""" TEST
m = 7
N = 143
d=47
C=mlucas(m,3,N)
print(C)
print(mlucas(C,d,N))
"""
N= 18378141703504870053256589621469911325593449136456168833252297256858537217774550712713558376586907139191035169090694633962713086351032581652760861668116820553602617805166170038411635411122411322217633088733925562474573155702958062785336418656834129389796123636312497589092777440651253803216182746548802100609496930688436148522617770670087143010376380205698834648595913982981670535389045333406092868158446779681106756879563374434867509327405933798082589697167457848396375382835193219251999626538126258606572805220878283429607438382521692951006432650132816122705167004219371235964716616826653226062550260270958038670427
C= 14470740653145070679700019966554818534890999807830802232451906444910279478539396448114592242906623394239703347815141824698585119347592990685923384931479024856262941313458084648914561375377956072245149926143782368239175037299219241806241533201175001088200209202522586119648246842120571566051381821899459346757935757111233323915022287370687524912870425787594648397524189694991735372527387329346198018567010117587531474035014342584491831714256980975368294579192077738910916486139823489975038981139084864837358039928972730135031064241393391678984872799573965150169368237298603189344477806873779325227557835790957023000991
e= 65537

print("[!] Factoring N (This may take some time...)")

p,q = fermat_factor(N)

print("[+] Factors found...")
print("p =", p)
print("q =", q)

d = get_privatekey(C,p,q,e)
# print(d)
m = LUC(C,d,N)
print(long_to_bytes(m))
```

## Flag
> UMASS{who_said_we_had_to_multiply_117a1b8a68814dc478ad78bc67d7d7d4}

## Ref

- https://en.wikipedia.org/wiki/Lucas_sequence
- https://en.wikipedia.org/wiki/Williams%27s_p_%2B_1_algorithm
- https://thescipub.com/pdf/jcssp.2008.1056.1060.pdf
