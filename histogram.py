#!/usr/bin/env python3

import collections
import sys

MAKE_CSV = False

def printUsage():
    print('./histogram [filename]')

# Get the filename from the command line
if len(sys.argv) == 2:
    fileName = sys.argv[1]
else:
    printUsage()

# Keep track of the total number of symbols so we can generate a frequency count
i = 0
e = 0
s = 0

# Create a histogram of every character in the given file
histogram = collections.Counter()

with open(fileName) as f:
    try:
        for line in f:
            try:
                username, password = line.split('\t')
                password = password.rstrip()

                for char in password:
                    histogram[char] += 1

                i += len(password)
            except:
                pass
    except UnicodeDecodeError:
        pass

# Output
if MAKE_CSV:
    for symbol, value in histogram.most_common():
        phi = value / float(i)
        print(symbol + ',' + str(value) + ',' + str(phi))
else:
    for symbol, value in histogram.most_common():
        phi = value / float(i)
        e += phi
        s += 1
        print(symbol, '=', value, '(', phi, ')')
    print(histogram)
    print('Combined length of ALL passwords =', i)
    print('Combined phi =', e)
    print('Combined symbols =', s)
