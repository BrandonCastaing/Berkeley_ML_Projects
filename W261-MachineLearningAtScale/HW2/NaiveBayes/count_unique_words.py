#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
    
INPUT:
    ID \t class \t header \t body
OUTPUT:
    unique_word_count
    
"""
import os
import re
import sys

word_hash = {}

# Read in each line of the document
for line in sys.stdin:
    # Note, this split_line logic was added to allow this mapper to be compatible with both the Chinese and Enron data formats
    # Specifically, Chinese data has precisely 1 text field while Enron has a Header + Body text field.
    split_line = line.rstrip().split('\t')
    if len(split_line) == 3:
        id_, class_, text = split_line
    else:
        id_, class_, header, body = split_line
        text = header + body
    
    words = re.findall(r'[a-z]+', text.lower())
    
    # Hashes create unique keys, thus unique words
    for word in words:
        word_hash[word] = word_hash.get(word, 0) + 1

# Output unique keys length
print(f"{len(word_hash.keys())}")