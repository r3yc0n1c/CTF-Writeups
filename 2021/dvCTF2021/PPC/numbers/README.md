# Numbers (98)
> nc challs.dvc.tf 3096

## Solution
The guessing game was based on **Integers** which seemed to be **random** everytime I connect to the server. As a wild guess, I thought maybe the backend script
is using **python** and it produces **32 bit integers** and the easiest way to do so is to use the **random** module. A fun fact about this module is that,

<p align='center'><b>
Python uses the Mersenne Twister as the core generator.
</b></p>

Now we have to crack this to predict the nest number. I used this - (https://github.com/kmyk/mersenne-twister-predictor) to predict the next state and get the flag.
***
Solve Script - [[guesser.py]](guesser.py)

Source Script - [[guess.py]](src/guess.py)
***

## Flag
> dvCTF{tw1st3d_numb3rs}

## Ref
- https://docs.python.org/3/library/random.html
- https://github.com/kmyk/mersenne-twister-predictor
