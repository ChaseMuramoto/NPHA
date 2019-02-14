import networkx as nx
from sklearn import cluster
from sklearn.cluster import KMeans
import pandas as pd
import operator
import numpy as np



#returns a list of list which will then be fed into the other algorithm
def create_clusters(num_buses, graph, capacity, constraints):
    
    k_clusters = num_buses
    
    model = cluster.KMeans(n_clusters=k_clusters, n_init=200)
    
    graph_copy, mapping, edge_mat = create_duplicate_graph_with_adjacency(graph)
    
    model.fit(edge_mat)
    
    cluster_map = pd.DataFrame()
    
    cluster_map['node_from_copy'] = list(graph_copy.nodes)
    cluster_map['cluster'] = model.labels_
    cluster_map['node_from_original'] = list(graph.nodes)
    
    clusters = {}
    clusters_that_exceed_capacity = []
    clusters_with_no_elements = []
    for i in range(num_buses):
        cluster_i = cluster_map[cluster_map.cluster == i]
        clusters[i] = cluster_i['node_from_original'].tolist()
        if len(clusters[i]) == 0:
            clusters_with_no_elements.append(i)
        if len(clusters[i]) > capacity:
            clusters_that_exceed_capacity.append(i)
    #check if any clusters have no elements

if len(clusters_that_exceed_capacity) == 0 and len(clusters_with_no_elements) == 0:
    return clusters
    elif len(clusters_that_exceed_capacity) > 0:
        nodes_to_add, clusters = remove_nodes_to_meet_capacity(clusters, clusters_that_exceed_capacity, capacity)
        print("remove nodes to meet cap used")
        if (len(clusters_with_no_elements) == 0):
            clusters = add_remainder_nodes(nodes_to_add, clusters, capacity)
            print("add remainder nodes was used")
        else:
            clusters = add_remainder_nodes_to_empty(nodes_to_add, clusters_with_no_elements, clusters, capacity)
            print("add remainder nodes to empty was used")

elif len(clusters_with_no_elements) > 0:
    clusters = fill_empty_clusters(clusters_with_no_elements, clusters)
    print("fill empty clusters was used")
    
    
    return clusters

### TODO:
def add_remainder_nodes(nodes_to_add, clusters, capacity):
    
    #take the nodes and add them to any clusters that aren't at capacity
    
    sorted_clusters = sorted(clusters, key = lambda k: len(clusters[k]))
    
    index = 0
    
    for k in sorted(clusters, key = lambda k: len(clusters[k])):
        curr_cluster = clusters[k]
        availability = capacity - len(curr_cluster)
        while availability > 0 and len(nodes_to_add) > 0:
            node = nodes_to_add.pop(0)
            curr_cluster.append(node)
            availability -= 1
        clusters[k] = curr_cluster
        if len(nodes_to_add) == 0:
            break
    return clusters

## TODO:
def add_remainder_nodes_to_empty(nodes_to_add, clusters_with_no_elements, clusters, size_bus):
    
    #first make sure that no nodes are empty by adding those nodes there first,
    #then randomly add to clusters that are not yet full
    while len(clusters_with_no_elements) > 0:
        if len(nodes_to_add) > 0:
            i = clusters_with_no_elements.pop(0)
            node = nodes_to_add.pop(0)
            clusters[i].append(node)

while len(clusters_with_no_elements) > 0:
    for c in range(len(clusters)):
        if len(clusters_with_no_elements) == 0:
            break
            while (len(clusters[c]) > 1):
                node = clusters[c].pop()
                empty_cluster = clusters_with_no_elements.pop()
                clusters[empty_cluster].append(node)
                if len(clusters_with_no_elements) == 0:
                    break

while len(nodes_to_add) > 0:
    for c in range(len(clusters)):
        if len(nodes_to_add) == 0:
            break
            while len(clusters[c]) < size_bus:
                node = nodes_to_add.pop(0)
                clusters[c].append(node)
                if len(nodes_to_add) == 0:
                    break
# node = nodes_to_add.pop(0)
# clusters[i].append(node)
# print('Bus being used: ' + str(i))
# print("Bus: " + str(clusters[i]))

return clusters

## TODO:
def fill_empty_clusters(clusters_with_no_elements, clusters):
    
    while len(clusters_with_no_elements) > 0:
        i = clusters_with_no_elements.pop(0)
        if len(clusters[i]) == 0:
            for j in clusters:
                if len(clusters[j]) > 1:
                    node = clusters[j].pop(0)
                    clusters[i].append(node)
                    break

return clusters
#sort the clusters that are the greatest in size, and then just add elements to the empty clusters_with_no_elements
#we should make this a smarter algorithm in the future by taking the node with fewest edges or one that causes a rowdy group

def remove_nodes_to_meet_capacity(clusters, clusters_that_exceed_capacity, capacity):
    nodes = []
    for bus in clusters_that_exceed_capacity:
        current_cluster = clusters[bus]
        amount = len(current_cluster) - capacity
        while(amount > 0):
            node = clusters[bus].pop(0)
            nodes.append(node)
            amount = amount - 1
    return nodes, clusters

#creates a copy of our graph, and then relabels those nodes
def create_duplicate_graph_with_adjacency(G):
    
    graph_copy = G.copy()
    sorted(graph_copy)
    number_of_nodes = len(list(graph_copy.nodes))
    
    mapping = dict(zip(graph_copy, range(0, number_of_nodes)))
    
    #graph is relabeled with node values 0 - number of nodes
    graph_copy = nx.relabel_nodes(graph_copy, mapping)
    
    edge_mat = np.zeros((len(G), len(G)), dtype=int)
    for node in graph_copy:
        for neighbor in graph_copy.neighbors(node):
            edge_mat[node][neighbor] = 1
        edge_mat[node][node] = 1
    
    return graph_copy, mapping, edge_mat
