from tsp import *

def find_mst2(graph: 'Graph'):
    edges = [(n1.point,n2.point,dist(n1,n2)) for n1,n2 in graph.get_edges()]
    edges = sorted(edges,key=lambda item: item[2])
    tree = []
    subtrees = UnionFind()
    for u,v,w in edges:
        tree.append((u,v,w))
        subtrees.union(u,v)
    return tree

class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object
        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]
        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest
