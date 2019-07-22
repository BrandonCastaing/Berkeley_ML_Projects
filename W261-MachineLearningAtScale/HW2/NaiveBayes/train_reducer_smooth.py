#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies
with plus one Laplace Smoothing.
    
INPUT:
    partition \t word \t class \t count
OUTPUT:
    word \t non_chinese_count,chinese_count,non_chinese_cond_prob,chinese_cond_prob
    
Instructions:
    Start by copying your unsmoothed reducer code
    (including the rest of the docstring info^^).
    Then make the necessary modifications so that you
    perform Laplace plus-k smoothing. See equation 13.7 
    in Manning, Raghavan and Shutze for details.
    
    Although we'll only look at results for K=1 (plus 1)
    smoothing its a good idea to set K as a variable
    at the top of your script so that its easy to change
    if you want to explore the effect of different 'K's.
    
    Please clearly mark the modifications you make to
    implement smoothing with a comment like:
            # LAPLACE MODIFICATION HERE 
"""
##################### YOUR CODE HERE ####################

import re
import sys

# initialize trackers + constants
k = 1.0
#unique_words = 6.0
unique_words = 4557.0

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
        # emit relative frequency
        if cur_word:
            # LAPLACE MODIFICATION HERE 
            non_chinese_cond_prob = (cur_nonchinese_count + k) / (total_nonchinese_words + unique_words)
            chinese_cond_prob = (cur_chinese_count + k) / (total_chinese_words + unique_words)
            print(f"{cur_word}\t{cur_nonchinese_count},{cur_chinese_count},{non_chinese_cond_prob},{chinese_cond_prob}")

        # start a new tally 
        cur_word, cur_count = word, int(value)
        if class_ == '1':
            cur_chinese_count = int(value)
            cur_nonchinese_count = 0
        else:
            cur_chinese_count = 0
            cur_nonchinese_count = int(value)
  
# print final word results
# LAPLACE MODIFICATION HERE 
non_chinese_cond_prob = (cur_nonchinese_count + k) / (total_nonchinese_words + unique_words)
chinese_cond_prob = (cur_chinese_count + k) / (total_chinese_words + unique_words)
print(f"{cur_word}\t{cur_nonchinese_count},{cur_chinese_count},{non_chinese_cond_prob},{chinese_cond_prob}")

# print Class priors
total_docs = total_nonchinese_docs + total_chinese_docs
print(f"ClassPriors\t{total_nonchinese_docs},{total_chinese_docs},{total_nonchinese_docs/total_docs},{total_chinese_docs/total_docs}")

##################### (END) CODE HERE ####################