#!/usr/bin/env python
"""
Mapper tokenizes and emits words with their class.
INPUT:
    ID \t SPAM \t SUBJECT \t CONTENT \n
OUTPUT:
    word \t class \t count 
"""
import re
import sys

# read from standard input
for line in sys.stdin:
    # parse input
    docID, _class, subject, body = line.split('\t')
    # tokenize
    words = re.findall(r'[a-z]+', subject + ' ' + body)
    
############ YOUR CODE HERE #########
    #word_class_hash = {}
    for word in words:
        #word_class_hash[f"{word}{_class}"] = word_class_hash.get(f"{word}{_class}", 0) + 1
        print(f"{word}\t{_class}\t1")

############ (END) YOUR CODE #########