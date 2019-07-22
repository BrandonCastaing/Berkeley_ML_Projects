#!/usr/bin/env python
"""
This script reads word counts from STDIN and combines
the counts for any duplicated words.

INPUT & OUTPUT FORMAT:
    word \t count
USAGE:
    python collateCounts.py < yourCountsFile.txt

Instructions:
    For Q6 - Use the provided code as is. (you'll need to uncomment it)
    For Q7 - Delete or comment out the section marked "PROVIDED CODE" &
             replace it with your own implementation. Your solution
             should not use a dictionary or store counts in any way -
             just print them as soon as you've added them. HINT: you've
             modified the framework script to ensure that the input
             is alphabetized; how can you use that to your advantage?
"""

# imports
import sys
from collections import defaultdict

########### PROVIDED IMPLEMENTATION ##############
##### uncomment to run
# counts = defaultdict(int)
# # stream over lines from Standard Input
# for line in sys.stdin:
#     # extract words & counts
#    word, count  = line.split()
#     # tally counts
#    counts[word] += int(count)
# # print counts
# for wrd, count in counts.items():
#    print("{}\t{}".format(wrd,count))
########## (END) PROVIDED IMPLEMENTATION #########

################# YOUR CODE HERE #################

curr_word = ""
curr_count = 0 
for line in sys.stdin:
    
    next_word, next_count  = line.split()
    
    # Add up repeating word's count
    if next_word == curr_word:
        curr_count += int(next_count)

    # When new word, output previous word's count
    else:
        print("{}\t{}".format(curr_word, str(curr_count)))
        curr_word = next_word
        curr_count = int(next_count)


################ (END) YOUR CODE #################
