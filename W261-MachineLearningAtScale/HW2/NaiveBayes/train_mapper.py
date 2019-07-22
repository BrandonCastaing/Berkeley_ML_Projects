#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
    
INPUT:
    ID \t class \t text
OUTPUT:
    partition \t word \t class \t count

Instructions:
    You know what this script should do, go for it!
    (As a favor to the graders, please comment your code clearly!)
    
    A few reminders:
    1) To make sure your results match ours please be sure
       to use the same tokenizing that we have provided in
       all the other jobs:
         words = re.findall(r'[a-z]+', text-to-tokenize.lower())
         
    2) Don't forget to handle the various "totals" that you need
       for your conditional probabilities and class priors.
"""
##################### YOUR CODE HERE ####################
import os
import re
import sys

total_chinese_docs = 0 
total_nonchinese_docs = 0 
total_chinese_words = 0
total_nonchinese_words = 0

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
    
    # Tokenize as suggested in Instructions
    words = re.findall(r'[a-z]+', text.lower())

    # Keep track of document totals
    if class_ == '1':
        total_chinese_docs += 1
    else:
        total_nonchinese_docs += 1
    
    # For each word
    for word in words:
        if class_ == '1':
            total_chinese_words += 1
        else:
            total_nonchinese_words += 1
        
        # Partition words by first letter
        if word[0] < 'i':
            print(f'A\t{word}\t{class_}\t1')
        elif word[0] < 'r':
            print(f'B\t{word}\t{class_}\t1')
        else:
            print(f'C\t{word}\t{class_}\t1')

# Lastly, Add totals to each partition
for part in ['A', 'B', 'C']:    
    print(f'{part}\t!totaldocs\t0\t{total_nonchinese_docs}')
    print(f'{part}\t!totaldocs\t1\t{total_chinese_docs}')
    print(f'{part}\t!totalwords\t0\t{total_nonchinese_words}')
    print(f'{part}\t!totalwords\t1\t{total_chinese_words}')
            
##################### (END) YOUR CODE #####################