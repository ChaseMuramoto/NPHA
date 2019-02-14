import networkx as nx
import os
from sklearn import cluster
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from annealers import SchoolBusProblem
import cluster_construction as cc
import random
import operator

# use kmeans clustering algorithm to
def solver(graph, num_buses, size_bus, constraints):
    
    # print("Number of Buses: " + str(num_buses))
    # print("Size of Buses: " + str(size_bus))
    # print("Rowdy Groups: ")
    # for group in constraints:
    #     print(str(group))
    #
    # print('-------------')
    
    bus_clusters = cc.create_clusters(num_buses, graph, size_bus, constraints)
    
    # print("Clusters: ")
    # for single_cluster in bus_clusters:
    #     print(str(single_cluster) + " --> " + str(bus_clusters[single_cluster]))
    #     print('-------------------')
    
    initial_state = [bus_clusters, constraints, graph, size_bus]
    tsp = SchoolBusProblem(initial_state)
    
    # tune annealing parameters
    tsp.Tmax = 50.0  # Max (starting) temperature, max number of rowdy groups violated
    tsp.Tmin = 1      # Min (ending) temperature, min number of rowdy groups violated
    tsp.steps = 10000   # Number of iterations
    tsp.updates = 50   # Number of updates (by default an update prints to stdout)
    
    tsp.state = [bus_clusters, constraints, graph, size_bus]
    final_state, score = tsp.anneal()
    
    return list(final_state[0].values()) # returns the list of clusters

#tells us which cluster each node is in
def make_node_map(clusters):
    n = {}
    for key, value in clusters.items():
        cluster_index = key
        for i in value:
            n[i] = cluster_index
    return n

def make_subgraph_map(clusters, graph):
    n = {}
    for key, value in clusters.items():
        cluster_index = key
        n[cluster_index] = graph.subgraph(list(value)).copy()
    return n

def return_clusters(cluster_map, num_buses):
    clusters = {}
    for i in range(num_buses):
        cluster_i = cluster_map[cluster_map.cluster == i]
        clusters[i] = cluster_i['node'].tolist()
    return clusters

def graph_to_edge_matrix(G):
    dicti = {}
    
    node_lookup = {}
    not_nums = []
    for node in G:
        try:
            current_node = int(node)
            node_lookup[node] = current_node
        except ValueError:
            not_nums.append(node)

current_node_value = max(node_lookup.items(), key=operator.itemgetter(1))[1] + 1

for string_node in not_nums:
    node_lookup[string_node] = current_node_value
    current_node_value = current_node_value + 1
    
    edge_mat = np.zeros((current_node_value + 1, current_node_value + 1), dtype = int)
    
    for node in G:
        valid_node = node_lookup[node]
        for neighbor in G.neighbors(node):
            valid_neighbor = node_lookup[neighbor]
            edge_mat[valid_node][valid_neighbor] = 1
        edge_mat[valid_node][valid_node] = 1
        dicti[valid_node] = edge_mat[valid_node]
    
    return edge_mat, dicti, node_lookup
