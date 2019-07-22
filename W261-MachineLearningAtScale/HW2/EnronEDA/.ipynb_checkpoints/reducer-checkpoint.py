#!/usr/bin/env python
"""
Reducer takes words with their class and partial counts and computes totals.
INPUT:
    word \t class \t partialCount 
OUTPUT:
    word \t class \t totalCount  
"""
import re
import sys

# initialize trackers
current_word = None
spam_count, ham_count = 0,0

# read from standard input
for line in sys.stdin:
    # parse input
    word, is_spam, count = line.split('\t')
    
############ YOUR CODE HERE #########
    if word != current_word:
        if current_word is not None:
            print(f"{current_word}\t0\t{ham_count}")
            print(f"{current_word}\t1\t{spam_count}")
        current_word = word
        spam_count, ham_count = 0,0
        
    if is_spam == '1':
        spam_count += 1
    else:
        ham_count += 1
    
print(f"{current_word}\t0\t{ham_count}")
print(f"{current_word}\t1\t{spam_count}")        
############ (END) YOUR CODE #########