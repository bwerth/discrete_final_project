# from functools import reduce
from tsp import *

# Based vaguely on:
# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/

# Use Kruskal's Algorithm to find Minimum Spanning Tree (MST)
# Node:
#   - point:
#       - Tuple, (x,y) assumed
#   - edges:
#       - set of points adjacent to node
#   - distance_to():
#       - returns distance to a node (weight?)
def find_mst(graph: 'Graph'):
    edges = [(n1,n2,dist(n1,n2)) for n1,n2 in graph.get_edges()] # unordered edges of graph
    num_nodes = len(graph.nodes)
    # num_edges = len(edges)
    result = [] # ordered list of nodes in the MST
    parent = []
    rank = []
    edges = sorted(edges,key=lambda item: item[2])
    for node in range(num_nodes):
        parent.append(node)
        rank.append(0)
    e = 0 # indexing for result[]
    i = 0 # indexing for edge sorting
    while e < num_nodes-1:
        u,v,w = edges[i]
        i = i+1
        x = findset(parent, u)
        y = findset(parent, v)
        if x != y:
            e = e+1
            result.append((u,v,w))
    return False

def findset(parent, i):
    if parent[i] == i:
        return i
    return findset(parent, parent[i])

def edge_union(parent,rank,x,y):
    xr = findset(parent,x)
    yr = findset(parent,y)
    if rank[xr] < rank[yr]:
        parent[xr] = yr
    elif rank[xr] > rank[yr]:
        parent[yr] = xr
    else:
        parent[yr] = xr
        rank[xr] = rank[xr]+1




















# oof
