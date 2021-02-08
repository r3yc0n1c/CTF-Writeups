# Unimplemented (100)
> A new publickey encryption algorithm is being invented, but the author is not quite sure how to implement the decryption routine correctly. Can you help him? <br>
> :arrow_down:  [unimplemented.py](unimplemented.py)

## Solution
After googling a lot about "Gaussian Integers" and "RSA" I found - [Modified RSA in the Domains of Gaussian Integers and Polynomials Over Finite Fields](https://www.researchgate.net/publication/220922838_Modified_RSA_in_the_Domains_of_Gaussian_Integers_and_Polynomials_Over_Finite_Fields)
which says,

<p align="center">
The φ function is a multiplicative function; i.e., φ(αβ) = φ(α)φ(β). Also, for a prime power Gaussian integer, the value of the φ function is <br><br>
φ(α<sup>n</sup>) = 2<sup>n</sup> − 2<sup>n−1</sup>, <br>
φ(π<sup>n</sup>) = q<sup>n−1</sup>(q − 1), <br>
or φ(p<sup>n</sup>) =  p<sup>2n−2</sup>(p<sup>2</sup> − 1). <br><br>
Thus, the  value  of φ  for  any  Gaussian  integer  β can be obtained from the prime power decomposition of  β. <br><br>
<b> φ(p<sup>n</sup>) =  p<sup>2n−2</sup>(p<sup>2</sup> − 1) </b>
</p>

Solve Script - [apex.py](apex.py)

## Other Resources
* [Crypto CTF 2019 / Complex RSA](https://sectt.github.io/writeups/CryptoCTF19/crypto_complexrsa/README)
* [Crypto CTF 2019 / Complex RSA - by Ariana1729](https://github.com/Ariana1729/CTF-Writeups/blob/master/2019/CryptoCTF/Complex%20RSA/README.md)
* [TetCTF 2021 Crypto Writeups - by rkm0959](https://rkm0959.tistory.com/192)
* [TetCTF 2021 Unimplemented - by LvMalware](https://github.com/LvMalware/CTF-WriteUps/blob/master/TetCTF/unimplemented.pdf)
