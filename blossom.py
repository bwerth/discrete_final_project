from tsp import *
from christofides import *
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

def minimum_weight_match(mst):
	odd_vertices = find_odd_verts(mst)
	random.shuffle(odd_vertices)
	while odd_vertices:
		v = odd_vertices.pop()
		length = float("inf")
		closest = 0
		for u in odd_vertices:
			if v != u and v.distance_to(u) < length:
				length = v.distance_to(u)
				closest = u
		is_in_mst = 0
		for edge in mst:
			if(edge[2] is v.distance_to(u)):
				if(edge[0],edge[1] is u,v or edge[0],edge[1] is v,u):
					is_in_mst = 1
		if(not is_in_mst):
			mst.add((u,v,v.distance_to(u)))
		odd_vertices.remove(u)
	return mst



