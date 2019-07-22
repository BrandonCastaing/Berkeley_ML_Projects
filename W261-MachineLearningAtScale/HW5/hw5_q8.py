#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" 
HW5 Q8 - wikiRDD Final Run
"""

# [START pyspark]
import pyspark
import re
import ast
import time
import numpy as np
import pandas as pd
from pyspark.accumulators import AccumulatorParam

print("Creating SparkContext")
sc = pyspark.SparkContext()

print("Importing wiki_graph.txt from GS URI")
wikiRDD = sc.textFile('gs://w261-castaing/wiki_graph.txt')

print("Successfully downloaded WikiRDD")

################################### FUNCTION DEFINITONS FROM hw5_workbook.ipynb
def initGraph(dataRDD):
    """
    Spark job to read in the raw data and initialize an 
    adjacency list representation with a record for each
    node (including dangling nodes).
    
    Returns: 
        graphRDD -  a pair RDD of (node_id , (score, edges))
        
    NOTE: The score should be a float, but you may want to be 
    strategic about how format the edges... there are a few 
    options that can work. Make sure that whatever you choose
    is sufficient for Question 8 where you'll run PageRank.
    """
    ############## YOUR CODE HERE ###############

    # write any helper functions here
    # Produces (node_id , (score, edges)) records
    def create_records(line):
        source_node, edges = line
        
        if len(edges) >= 1:
            # Reconstructs edge hash from custom comma-delimited string
            edge_strings = edges.split(',')
            edge_hash = {}
            for edge_weight in edge_strings:
                # Each node and its weight are seperated by a dash
                split = edge_weight.split('-')
                edge_hash[split[0]] = split[1] 

            yield (source_node, (1/node_count_b.value, edge_hash))
        
        # Output for Dangling Node
        else:
            yield (source_node, (1/node_count_b.value, {}))
            
    # Produces records with a Node ID as the Key and an edges hash as the value
    def parse_edge_hashes(line):
        source_node, edge_nodes = line.split('\t')
        
        edges = ast.literal_eval(edge_nodes)
        
        # Tried using a Hash directly, but this seemed to cause memory errors... Using a complex string object to conserve memory usage
        edge_dash = ''
        for key, value in edges.items():
            edge_dash += f"{key}-{value},"
        edge_dash = edge_dash[:-1]
            
        yield (int(source_node), edge_dash)
        
        for edge in edges.keys():
            yield (int(edge), '')
    
    # Combines 2 strings into 1 string
    def reduce_strings(x,y):
        combined = f"{x},{y}"
        
        # Removes tailing and starting commas resulting from one record being empty string
        if combined[-1] == ',':
            combined = combined[:-1]
        elif combined[0] == ',':
            combined = combined[1:]
            
        return combined
            
    # write your main Spark code here    
    
    # Create RDD with records of (SourceNodeId, EdgesHash)
    node_edges_rdd = dataRDD.flatMap(parse_edge_hashes).reduceByKey(reduce_strings).cache()

    # Count total # of nodes
    node_count = node_edges_rdd.count()
    node_count_b = sc.broadcast(node_count)

    # Compute probabilities and populate resulting RDD
    graphRDD = node_edges_rdd.flatMap(create_records)
    
    ############## (END) YOUR CODE ##############
    
    return graphRDD


class FloatAccumulatorParam(AccumulatorParam):
    """
    Custom accumulator for use in page rank to keep track of various masses.
    
    IMPORTANT: accumulators should only be called inside actions to avoid duplication.
    We stringly recommend you use the 'foreach' action in your implementation below.
    """
    def zero(self, value):
        return value
    def addInPlace(self, val1, val2):
        return val1 + val2

    
# part d - job to run PageRank (RUN THIS CELL AS IS)
def runPageRank(graphInitRDD, alpha = 0.15, maxIter = 10, verbose = True):
    """
    Spark job to implement page rank
    Args: 
        graphInitRDD  - pair RDD of (node_id , (score, edges))
        alpha         - (float) teleportation factor
        maxIter       - (int) stopping criteria (number of iterations)
        verbose       - (bool) option to print logging info after each iteration
    Returns:
        steadyStateRDD - pair RDD of (node_id, pageRank)
    """
    # teleportation:
    a = sc.broadcast(alpha)
    
    # damping factor:
    d = sc.broadcast(1-a.value)
    
    # initialize accumulators for dangling mass & total mass
    mmAccum = sc.accumulator(0.0, FloatAccumulatorParam())
    totAccum = sc.accumulator(0.0, FloatAccumulatorParam())
    
    ############## YOUR CODE HERE ###############
    
    #reads in each record and redistributes the node's current score to each of its neighbors
    #uses an accumulator to add up the dangling node mass and redistribute it among all the nodes. (Don't forget to reset this accumulator after each iteration!)
    #uses an accumulator to keep track of the total mass being redistributed.( This is just for your own check, its not part of the PageRank calculation. Don't forget to reset this accumulator after each iteration.)
    #aggregates these partial scores for each node
    #applies telportation and damping factors as described in the formula above.
    #combine all of the above to compute the PageRank as described by the formula above.
    #WARNING: Some pages contain multiple hyperlinks to the same destination, please take this into account when redistributing the mass.
    
    # write your helper functions here, 
    # please document the purpose of each clearly 
    # for reference, the master solution has 5 helper functions
    
    # Mapper function to convert a (node_id , (score, edges)) record into (node_id, edge_hash) and (node_id, score) records
    def disperse_mass(node_record):
        curr_node, mass_edge_tuple = node_record
        curr_mass, edge_hash = mass_edge_tuple
        
        # Add current node mass to Total Mass
        totAccum.add(float(curr_mass))
        
        edge_count = len(edge_hash.keys())
        if edge_count == 0:
            # Dangling Node - Add to mmAcum
            mmAccum.add(float(curr_mass))
        else:
            # Nondangling - Disperse mass over current edges
            # Calculation to use edge weights
            weight_sum = 0
            for val in edge_hash.values():
                weight_sum += int(val)
            partial_mass = float(curr_mass / weight_sum)

            for edge, weight in edge_hash.items():
                yield (int(edge), float(curr_mass / edge_count)) 
        yield (curr_node, edge_hash)
                
    # Combiner function to combine (node_id, edge_hash) and (node_id, score) records back into a (node_id , (score, edges)) record        
    def combine(grouping):
        node_id, records = grouping
        mass = 0.0
        edges = ''

        for record in records:
            if type(record) == dict:
                # Avoid updating hash by recreating and updating string
                for key, value in record.items():
                    edges += f"{key}-{value},"
            else:
                mass += float(record)

        edge_hash = {}
        if edges != '':
            # Reconstruct hash
            if edges[-1] == ',':
                edges = edges[:-1]

            for edge_weight in edges.split(','):
                # Each node and its weight are seperated by a dash
                split = edge_weight.split('-')
                edge_hash[split[0]] = split[1] 

        return (node_id, (mass, edge_hash))
    
    # Function that computes PageRank metric for each Node record
    def compute_page_rank(node_record):
        node_id, mass_tuple = node_record
        mass, edges = mass_tuple
        
        mm = mm_b.value
        node_count = count_b.value
        teleportation = a.value
        dampening = d.value
        
        page_rank = (teleportation * float(1/node_count)) + (dampening * (float(mm/node_count) + mass))
        
        return (node_id, (page_rank, edges))
    
    # Transforms (node_id , (score, edges)) records into (node_id , score) which is the expected output
    def remove_edges(node_record):
        node_id, mass_tuple = node_record
        mass = mass_tuple[0]
        return (node_id, mass)
        
            
    # write your main Spark Job here (including the for loop to iterate)
    # for reference, the master solution is 21 lines including comments & whitespace
    node_count = graphInitRDD.count()
    print(f"Node Count: {node_count}")
    count_b = sc.broadcast(node_count)
    
    nodeMassRDD = graphInitRDD
    for i in range(1, maxIter+1): 
        # Map
        nodeMassRDD = nodeMassRDD.flatMap(disperse_mass).groupByKey().map(combine)

        # Reduce
        nodeMassRDD.foreach(print)

        mm_b = sc.broadcast(mmAccum.value)
        #if verbose:
        print(f"{time.time()} Iteration {i} - Total Mass: {totAccum.value}, Missing Mass: {mmAccum.value}")

        # Compute PageRank
        nodeMassRDD = nodeMassRDD.map(compute_page_rank)
        
        # Reset accumulators
        mmAccum = sc.accumulator(0.0, FloatAccumulatorParam())
        totAccum = sc.accumulator(0.0, FloatAccumulatorParam())

    steadyStateRDD = nodeMassRDD.map(remove_edges)
    
    ############## (END) YOUR CODE ###############
    
    return steadyStateRDD
########################################### END FUNCTION DEFINITIONS

# Initialize graph from wikiRDD
start = time.time()
wikiGraphRDD = initGraph(wikiRDD)
print(f'... full graph initialized in {time.time() - start} seconds')

# Calculate PageRank for wikiRDD
nIter = 10
start = time.time()
full_results = runPageRank(wikiGraphRDD, alpha = 0.15, maxIter = nIter, verbose = True)
print(f'...trained {nIter} iterations in {time.time() - start} seconds.')
print(f'Top 20 ranked nodes:')
print(full_results.takeOrdered(20, key=lambda x: -x[1]))

# [END pyspark]