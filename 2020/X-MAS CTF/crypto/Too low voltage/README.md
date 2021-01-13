# Too low voltage (435)
> We fixed a major issue in the factory, but now we have a partial power outage, so everything is running low on power. <br>
> We need everything to be online, so we can't really afford shutting down any of our machines... It seems all our encryption engines are  <br> 
> working fine, so apparently our generators lacking a few volts doesn't hurt anyone. You can check them if you want, but I'm sure they are all fine. <br>
> :arrow_down:  [TooLow.zip](TooLow.zip)

## The Vulnerability ( Low Voltage Attack on RSA!!! (a.k.a Bellcore attack) )
RSA-CRT transforms message m into signature s using private key **p, q, dp, dq** as follows:

<p align="center">
    sp = ( mp )<sup>dp</sup> mod p, <br>
    sq = ( mq )<sup>dq</sup> mod q, <br>
    s = ( ( (sq – sp) · pinv)mod q)· p + sp,
</p>

where **mp = m mod p, mq = m mod q, pinv = p<sup>–1</sup>mod q**. Suppose either  **sp**  or  **sq**  is computed with a fault. Assume that the resulting faulty 
signature  **s'**  together with the correct signature **s** are known to the attacker. Then he can retrieve the private key by computing 

<p align="center">
    gcd(s – s', N)
</p>

## Implementation
* Solve Script - [apex.py](apexx.py)

## Flag
> **X-MAS{Oh_CPU_Why_h4th_th0u_fors4k3n_u5_w1th_b3llc0r3__th3_m4th_w45_p3rf3c7!!!_2194142af19aeea4}**

## Ref
* https://maxime.puys.name/publications/pdf/PRBL14.pdf
* https://eprint.iacr.org/2012/553.pdf
