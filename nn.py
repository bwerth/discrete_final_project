from tsp import (
    Node,
    Graph,
    SvgGraph,
    dist,
)

import random


def nearest_neighbor_sort(graph: Graph) -> Node:
    def follow_path(n: Node):
        if len(n.edges) > 1:
            raise ValueError('Start {!r} has more than one edge'.format(n))
        if len(n.edges) == 0:
            return n
        last = n
        selected = next(iter(n.edges))
        while len(selected.edges) != 1:
            if len(selected.edges) != 2:
                raise ValueError('Inner {!r} does not have two edges'.format(selected))
            next_node = next(iter(selected.edges.difference({last})))
            last = selected
            selected = next_node
        return selected
    picked = set()
    # we only want to connect nodes on the end of a path, not in the middle
    end_nodes = set(filter(lambda n: len(n.edges) <= 1, graph.nodes))
    # pick a node to start from
    start = random.choice(list(end_nodes))  # TODO: find a better way to get a random element
    selected = follow_path(start)
    picked.add(selected)
    picked.add(start)
    remaining = end_nodes.difference(picked)
    while len(remaining) != 0:
        next_node = min(remaining, key=lambda n: dist(selected, n))
        # follow node to the end of its path
        end = follow_path(next_node)
        selected.connect(next_node)
        picked.add(next_node)
        picked.add(end)
        selected = end
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
