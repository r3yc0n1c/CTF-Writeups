#!/usr/bin/env ruby

WORDS       = File.read(File.join(__dir__, 'words.txt')).split(/\n/)

for i in 0..1024
	# word = WORDS.sample()
	word = rand(0xFFFFFFFF)
	# puts ";) WORD -> #{word} -> #{WORDS.index(word)}"
	puts "#{word} -> #{word & 0xFFFF} | #{word >> 16}"
end