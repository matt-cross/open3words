# open3words
Stupid simple open-source reimplementation of what3words

Usage: open3words.py [<lat,lon> [<three.word.phrase] ...]

Main public python interface functions that are exported are:
 * words_to_latlon(words) - Pass in a 3 word phrase, returns the lat,lon in a tuple

 * latlon_to_words(lat,lon) - Pass in latitude and longitude as floats, returns a 3 word phrase as a
                              string.
