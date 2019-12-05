from tsp import *
import random
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
def find_odd_vertices(graph: 'Graph'):
	odd_vertices = {}
	for node in graph.nodes:
		connections = len(node.edges)
		if(connections%2 is 1):
			odd_vertices.add(node)
	return odd_vertices

def minimum_weight_match(graph: 'Graph',mst):
	odd_vertices = find_odd_vertices(graph)
	random.shuffle(odd_vertices)

	while odd_vertices:
		v = odd_vertices.pop()
		length = float("inf")
		closest = 0
		for u in odd_vertices:
			if v != u and v.distance_to(u) < length:
				length = v.distance_to(u)
				closest = u
		if(not mst.nodes[u].is_connected(mst.nodes[v])):
			mst.nodes[u].connect(mst.nodes[v])
		odd_vertices.remove(u)




