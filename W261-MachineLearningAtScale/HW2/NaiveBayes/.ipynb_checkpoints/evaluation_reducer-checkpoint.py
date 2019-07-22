#!/usr/bin/env python
"""
Reducer to calculate precision and recall as part
of the inference phase of Naive Bayes.
INPUT:
    ID \t true_class \t P(ham|doc) \t P(spam|doc) \t predicted_class
OUTPUT:
    # Documents \t ##
    True Positives \t ##
    True Negatives \t ##
    False Positives \t ##
    False Negatives \t ##
    Accuracy \t ##
    Precision \t ##
    Recall \t ##
    F-Score \t ##
         
Instructions:
    Complete the missing code to compute these^ four
    evaluation measures for our classification task.
    
    Note: if you have no True Positives you will not 
    be able to compute the F1 score (and maybe not 
    precision/recall). Your code should handle this 
    case appropriately feel free to interpret the 
    "output format" above as a rough suggestion. It
    may be helpful to also print the counts for true
    positives, false positives, etc.
"""
import sys

# initialize counters
FP = 0.0 # false positives
FN = 0.0 # false negatives
TP = 0.0 # true positives
TN = 0.0 # true negatives
doc_total = 0.0

# read from STDIN
for line in sys.stdin:
    # parse input
    docID, class_, pHam, pSpam, pred = line.split()
    # emit classification results first
    print(line[:-2], class_ == pred)
    
    # then compute evaluation stats
#################### YOUR CODE HERE ###################
    doc_total += 1.0

    if pred == '1' and class_ == '1':
        TP += 1.0
    elif pred == '0' and class_ == '0':
        TN += 1.0
    elif pred == '1' and class_ == '0':
        FP += 1.0
    else:
        FN += 1.0

# Calculate performance metrics safely
if TP + FP == 0.0:
    precision = 0.0
else:
    precision = TP / (TP + FP)

if TP + FN == 0.0:
    recall = 0.0
else:
    recall = TP / (TP + FN)

accuracy = (TP + TN) / (TP + TN + FP + FN)

if precision + recall == 0.0:
    f_score = 0.0
else:
    f_score = 2 * ((precision * recall) / (precision + recall))
    
# Output performance metrics
print(f"# Documents \t {doc_total}")
print(f"True Positives \t {TP}")
print(f"True Negatives \t {TN}")
print(f"False Positives \t {FP}")
print(f"False Negatives \t {FN}")
print(f"Accuracy \t {accuracy}")
print(f"Precision \t {precision}")
print(f"Recall \t {recall}")
print(f"F-Score \t {f_score}")
#################### (END) YOUR CODE ###################
    