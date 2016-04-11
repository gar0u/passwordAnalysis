#!/usr/bin/env python3

import datetime
import sys
from collections import Counter
from math import log

startTime = datetime.datetime.now()

c = Counter()

bad = 0
good = 0
lines = 0
EXPECTED_ENTROPY = 6.4753	# bits
DEBUG = True

with open('10-million-combos.txt') as f:
    try:
        for line in f:
            lines += 1
            try:
                username, password = line.split('\t')
        
                c[password.rstrip()] += 1 
                good += 1
            except:
                pass
    except UnicodeDecodeError:
        bad += 1
        pass

# There are 89 unique symbols across all the passwords (according to my 'histogram' script, 
# so the entropy per character is 6.47573 bits, i.e. log_2(89)
# The ideal entropy of a 8-character password would be 6.47573 * 8 = round(51.8 bits) = 52 bits
# In reality, the top ten passwords are between 0 (min) and 3.16993 (max) bits.

# Calculate the entropy of each unique password and store it in a dictionary
actualEntropy = Counter()
expectedEntropy = Counter()

for entry in c.most_common():
    password, count = entry

    # 1. Symbol frequency
    symbols = Counter()
    for char in password:
        symbols[char] += 1
    n = len(password)

    # 2. List of probabilities (mapping to symbols is not needed for entropy calculation)
    probabilities = []
    for entry in symbols.most_common():
        probabilities.append(float(entry[1]) / n)

    # 3. Calculate Shannon entropy (number of bits / symbol)
    H = 0
    for probability in probabilities:
        H += - (probability * log(probability, 2))
    
    # 4. Store password and entropy
    actualEntropy[password] = H * n
    expectedEntropy[password] = EXPECTED_ENTROPY * n

# Output some statistics (for debugging)
if DEBUG:
    print('Good password count =', good)
    print('Bad password count =', bad)
    print('Line count =', lines)
    print('Unique passwords =', len(c))

    print('Top 10 Passwords:')
    print(c.most_common(10))

    endTime = datetime.datetime.now()
    print('Finished!  Runtime =', str(endTime - startTime))

# Output a CSV for analysis
# PASSWORD, ENTROPY_EXPECTED, ENTROPY_ACTUAL
else:
    for entry in actualEntropy.most_common():
        password, H = entry
        # print(password + ',' + str(expectedEntropy[password]) + ',' + str(H))
        print(str(expectedEntropy[password]) + ',' + str(H))
