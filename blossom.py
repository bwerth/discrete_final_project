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

def dist_verts(u,v):
	return math.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

def minimum_weight_match(mst,graph):
	odd_vertices = find_odd_verts(mst)
	random.shuffle(odd_vertices)
	while odd_vertices:
		v = odd_vertices.pop()
		length = float("inf")
		closest = 0
		for u in odd_vertices:
			if(v != u and dist_verts(u,v) < length):
				length = dist_verts(u,v)
				closest = u
		is_in_mst = 0
		for edge in mst:
			if(edge[2] is dist_verts(u,v)):
				if(edge[0],edge[1] is u,v or edge[0],edge[1] is v,u):
					is_in_mst = 1
		if(not is_in_mst):
			mst.append(dist_verts(u,v))
		odd_vertices.remove(u)
	return mst
