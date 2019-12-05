from tsp import (
    Node,
    Graph,
    SvgGraph,
    dist,
)

import random


def nearest_neighbor_sort(graph: Graph) -> Node:
    picked = set()
    # we only want to connect nodes on the end of a path, not in the middle
    end_nodes = set(filter(lambda n: len(n.edges) <= 1, graph.nodes))
    # pick a node to start from
    start = random.choice(list(end_nodes))  # TODO: find a better way to get a random element
    selected = start
    picked.add(selected)
    remaining = end_nodes.difference(picked)
    while len(remaining) != 0:
        next_node = min(remaining, key=lambda n: dist(selected, n))
        selected.connect(next_node)
        selected = next_node
        picked.add(selected)
        remaining = end_nodes.difference(picked)
    return start


if __name__ == '__main__':
    d = [
        [(0, 0), (1, 1)],  # simple two-point line
        [(0, 0), (0, 1), (1, 2), (2, 3), (0, 0)],  # a cycle
        [(1, 2), (4, 5), (2, 3)],  # a bent three-point line
    ]
    g = Graph.from_drawing(d)

    start = nearest_neighbor_sort(g)
