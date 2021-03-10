#!/bin/bash

sudo apt -y install ruby-full
sudo gem install colorize

echo -ne '#!/usr/bin/env ruby\n\nFLAG = "CTF{<|_kudos_you_win_|>}"' > flag.rb
chmod +x hangman.rb