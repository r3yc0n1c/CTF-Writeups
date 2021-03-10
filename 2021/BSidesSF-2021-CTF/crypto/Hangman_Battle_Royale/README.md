# Hangman Battle Royale (751)
![badge](https://img.shields.io/badge/Post%20CTF-Writeup-success)
> Can you win at least 8 rounds of Hangman? <br>
> `nc -v hangman-battle-royale-2d147e0d.challenges.bsidessf.net 2121` <br>
> (author: iagox86) <br>
> :arrow_down: [chall.zip](chall.zip)

## Solution
The interesting parts of the `hangman.rb` file and i commented them for better understanding...
```rb
#!/usr/bin/env ruby

[spin]

def get_opponents(count)
  return 0.upto(count-1).map do ||
    i = rand(0xFFFFFFFF)        # Use of rand() in ruby which 
    "#{ FIRST_NAMES[i & 0xFFFF] } #{ LAST_NAMES[i >> 16] }"     # (i & 0xFFFF) = LSB half of i and (i >> 16) = MSB half of i
  end
end

def play_round(opponents, round)
  # Pick a word
  word = WORDS.sample()     # picks random word from the array of words (the index is a 16 bits num everytime) 

  # Make sure there are an odd number of opponents
  if (opponents.length % 2) == 0
    puts "Somehow, we ended up with an invalid number of opponents!".red
    exit(1)
  end

  puts
  puts "================================".blue
  puts "         ROUND #{round}!".blue
  puts "================================".blue
  puts

  puts "This game's match-ups are:"
  puts
  opponents.each_slice(2) do |s|
    if s.length == 2
      puts "#{ s[0].ljust(20) }  -vs-  #{ s[1] }"
    else
      puts
      puts "And finally..."
      puts
      puts "#{ "YOU".ljust(20) } -vs-  #{ s[0] }!"
    end
  end

  puts
  puts "GOOD LUCK!!"
  puts
  #puts "HINT: #{word}-------------------------------------------------------"


  revealed = '_' * word.length()
  loop do
    revealed = player_turn(revealed, word)
    if revealed.index('_').nil?
      break
    end

    revealed = computer_turn(revealed, word)
    if revealed.index('_').nil?
      puts "Sorry, you lost! Please try again later".red
      exit(0)
    end
  end

  puts
  puts "    #{ revealed.chars().map { |c| c.underline() }.join(' ') }"
  puts

  puts "Congratulations, you beat #{ opponents.pop } and won this round! Let's see how the others did!".green
  puts
  puts "Press enter to continue"
  gets

  # Remove your opponent
  opponents = opponents.each_slice(2).map do |s|
    if rand() < 0.5
      puts "#{ s[0].green } beat #{ s[1].red } and moves on to the next round!"
      s[0]
    else
      puts "#{ s[1].green } beat #{ s[0].red } and moves on to the next round!"
      s[1]
    end
  end

  puts "Press enter to continue"
  gets

  return opponents
end

def start_game()
  puts "Welcome to Hangman Battle Royale!"
  puts
  puts "================================"
  puts "           MAIN MENU"
  puts "================================"
  puts

  puts "How many rounds do you want to play? (2 - 16)"
  puts
  puts "If you play at least 8 rounds, you win the special prize!"
  puts
  rounds = get_number()

  # Opponents are two to the number of rounds
  opponent_count = (2**rounds) - 1
  if opponent_count > 65536
    puts "That's too many rounds!".red
    return
  end

  opponents = get_opponents(opponent_count)
  round = 1
  loop do
    opponents = play_round(opponents, round)

    # If the player losers, play_round returns null
    if !opponents
      puts "Sorry, you lose! :(".red
      return
    end

    if opponents.length() == 0
      puts "You win this round!".green.bold

      if rounds >= 8
        puts "Wow, that was a MEGA victory!".green
        puts "Flag: #{ FLAG }".green
        exit
      end

      return
    end

    round += 1
  end
end

start_game()
```

After a little bit of googling we can find that
```
Random number generation in Ruby uses Mersenne Twister as a pseudo-random number sequence generator.
```
Now we can assume that `rand()` in ruby might use **mt19937** and already there are tools to crack this. I used this one
- [Mersenne Twister Predictor](https://github.com/kmyk/mersenne-twister-predictor)

But the main challenge was to predict the next word as the indices of the **words** used in every ROUND seem to be **16 bits** integers.
Then in the Slack Channel the Author said we can use 
```py
index = predicted_32_bit_int & 0xFFFF
predicted_WORD = WORDS[index]
```
i.e. the LSB half of the predicted index will match the **original word** index.

Full Solution Script - [[apex.py]](apex.py)

## Ref
* https://en.wikipedia.org/wiki/Mersenne_Twister
