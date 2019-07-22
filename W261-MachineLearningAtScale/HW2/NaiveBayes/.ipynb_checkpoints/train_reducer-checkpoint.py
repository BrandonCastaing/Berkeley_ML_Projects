#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies.
    
INPUT:
    partition \t word \t class \t count
OUTPUT:
    word \t non_chinese_count,chinese_count,non_chinese_cond_prob,chinese_cond_prob
    
Instructions:
    Again, you are free to design a solution however you see 
    fit as long as your final model meets our required format
    for the inference job we designed in Question 8. Please
    comment your code clearly and concisely.
    
    A few reminders: 
    1) Don't forget to emit Class Priors (with the right key).
    2) In python2: 3/4 = 0 and 3/float(4) = 0.75
"""
##################### YOUR CODE HERE ####################

import re
import sys

# initialize trackers
cur_word = None
cur_count = 0.0
cur_chinese_count = 0.0
cur_nonchinese_count = 0.0

total_chinese_docs = 0.0
total_nonchinese_docs = 0.0 

total_chinese_words = 0.0
total_nonchinese_words = 0.0

# read input key-value pairs from standard input
for line in sys.stdin:
    partition, word, class_, value = line.rstrip().split()
    
    # store Doc count total
    if word == '!totaldocs':  
        if class_ == '1':
            total_chinese_docs += float(value)
        else:
            total_nonchinese_docs += float(value)
        continue

    # store Word count total
    if word == '!totalwords':  
        if class_ == '1':
            total_chinese_words += float(value)
        else:
            total_nonchinese_words += float(value)
        continue

    # tally counts from current key
    if word == cur_word: 
        cur_count += float(value)
        if class_ == '1':
            cur_chinese_count += float(value)
        else: 
            cur_nonchinese_count += float(value)
    
    # OR ...  
    else:        
        # emit naive bayes model parameters
        if cur_word:
            non_chinese_cond_prob = cur_nonchinese_count / total_nonchinese_words
            chinese_cond_prob = cur_chinese_count / total_chinese_words
            print(f"{cur_word}\t{cur_nonchinese_count},{cur_chinese_count},{non_chinese_cond_prob},{chinese_cond_prob}")

        # start a new tally 
        cur_word, cur_count = word, float(value)
        if class_ == '1':
            cur_chinese_count = float(value)
            cur_nonchinese_count = 0
        else:
            cur_chinese_count = 0
            cur_nonchinese_count = float(value)
  
# print final word results
non_chinese_cond_prob = cur_nonchinese_count / total_nonchinese_words
chinese_cond_prob = cur_chinese_count / total_chinese_words
print(f"{cur_word}\t{cur_nonchinese_count},{cur_chinese_count},{non_chinese_cond_prob},{chinese_cond_prob}")

# print Class priors
total_docs = total_nonchinese_docs + total_chinese_docs
print(f"ClassPriors\t{total_nonchinese_docs},{total_chinese_docs},{total_nonchinese_docs/total_docs},{total_chinese_docs/total_docs}")

##################### (END) CODE HERE ####################