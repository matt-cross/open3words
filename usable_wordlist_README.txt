The file 'usable_wordlist.txt' is a filtered version of words_alpha.txt from https://github.com/dwyl/english-words

This list consists of all words in the last except for:
* All words of 2 letters or less
* All words of 10 letters or more
* All words with doubled letters in them

It was created with this one-liner shell command:

grep -E '^[a-z]{3,}' ../english-words/words_alpha.txt | grep -v -E '([a-z])\1' | grep -v -E '[a-z]{10,}' > usable_wordlist.txt
