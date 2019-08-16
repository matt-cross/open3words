#!/usr/bin/env python

import sys

# This word list has about 160000 words
words = [line.strip() for line in open('usable_wordlist.txt', 'r').readlines()]

numwords = 80000
assert len(words) >= numwords*2

# We divide each degree of latitude and longitude into 37,000 subdivisions to give us roughly 3m
# resolution.
divs_per_degree = 37000

# Given a latitude and longitude in a floating number, convert it to a rectangle number, where the
# rectangles are roughly 3m square (on the equator at least, they get smaller and warp as you get
# off the equator, but whatever).
def latlon_to_rectnum(lat, lon):
    assert (lat >= -90) and (lat <= 90)
    assert (lon >= -180) and (lon <= 180)

    latline = int((lat + 90) * divs_per_degree)
    lonline = int((lon + 180) * divs_per_degree)

    return latline * (400 * divs_per_degree) + lonline

# Given a rectangle number, convert it into 3 words from our wordlist.  Returns a string containing
# the 3 words separated by a '.'
def rectnum_to_words(rectnum):
    assert rectnum <= numwords * numwords * numwords

    idx1 = int(rectnum % numwords)
    idx2 = int((rectnum / numwords) % numwords)
    idx3 = int(rectnum / numwords / numwords)

    # Our wordlist has about twice as many words as we need, to multiply by 2 to use the whole range
    # of words
    return words[idx3 * 2] + '.' + words[idx2 * 2] + '.' + words[idx1 * 2]

# This is the normal public method to convert a latitute and longitude into 3 words separated by a
# '.'.
def latlon_to_words(lat, lon):
    return rectnum_to_words(latlon_to_rectnum(lat, lon))

# This performs the opposite of latlon_to_rectnum() - given a rectangle number, it converts it into
# an approximate latitude and longitude.
def rectnum_to_latlon(rectnum):
    lonline = rectnum % (400 * divs_per_degree)
    latline = rectnum / (400 * divs_per_degree)

    lon = float(lonline) / float(divs_per_degree) - 180
    lat = float(latline) / float(divs_per_degree) - 90

    return (lat,lon)

# This performs the opposite of rectnum_to_words() - given a string with 3 words from our wordlist
# separated by dots, it returns the rectangle number associated with it.
def words_to_rectnum(words_in):
    splitwords = words_in.split('.')
    assert len(splitwords) == 3

    # We multiplied by 2 when indexing into the list above, so we must divide by two here.
    idx3 = words.index(splitwords[0]) / 2
    idx2 = words.index(splitwords[1]) / 2
    idx1 = words.index(splitwords[2]) / 2

    return idx3 * numwords * numwords + idx2 * numwords + idx1

# This is the public method to convert 3 words into a latitude and longitude, it does the inverse of
# latlon_to_words() above.
def words_to_latlon(words):
    return rectnum_to_latlon(words_to_rectnum(words))

# Generic conversion function: takes a string and returns a string.  If the input string is a
# 'lat,lon' pair, this will return 3 words corresponding to that latitude and longitude.  If the
# input string is 3 words separated by a '.', it will return a 'lat,lon' string.  Otherwise it will
# return the string 'ERROR'.
def generic_convert(s):
    latlon_maybe = s.split(',')
    if len(latlon_maybe) == 2:
        return latlon_to_words(float(latlon_maybe[0]), float(latlon_maybe[1]))
    elif len(s.split('.')) == 3:
        result = words_to_latlon(s)
        return '{},{}'.format(result[0], result[1])
    else:
        return 'ERROR'

if __name__ == '__main__':
    for s in sys.argv[1:]:
        print generic_convert(s)
