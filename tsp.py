import abc
from typing import Tuple, List, Set, Iterable, FrozenSet
import math
import itertools

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from svgpathtools import svg2paths, wsvg


# type definitions
Point = Tuple[float, float]
Path = List[Point]

Drawing = List[Path]


class Solvable(abc.ABC):
    def distance_to(self, other: 'Solvable') -> float:
        pass


def dist(one: Solvable, other: Solvable) -> float:
    return one.distance_to(other)


class Node(Solvable):
    def __init__(self, point: Point):
        self.point = point
        self.edges = set()

    def distance_to(self, other: 'Node') -> float:
        # TODO: look into <https://docs.python.org/3/library/functools.html#functools.lru_cache>
        # for this
        return math.sqrt((self.point[0] - other.point[0])**2 + (self.point[1] - other.point[1])**2)

    def connect(self, other: 'Node'):
        self.edges.add(other)
        other.edges.add(self)

    def is_connected(self, other: 'Node') -> bool:
        assert (other in self.edges) == (self in other.edges)
        return self in other.edges

    def __str__(self) -> str:
        return 'Node({!r})<id={!r}>'.format(self.point, str(id(self))[-4:])

    def __repr__(self) -> str:
        return str(self)


class Graph(object):
    def __init__(self):
        self.nodes = set()

    @classmethod
    def from_drawing(cls, d: Drawing) -> 'Graph':
        return cls.from_paths(d)

    @classmethod
    def from_paths(cls, ps: Iterable[Path]) -> 'Graph':
        g = cls()
        for path in ps:
            subg = cls.from_path(path)
            g.nodes.update(subg.nodes)
        return g

    @classmethod
    def from_path(cls, p: Path) -> 'Graph':
        g = cls()
        p = iter(p)
        node_a = Node(next(p))
        g.nodes.add(node_a)
        for point in p:
            node_b = Node(point)
            node_b.connect(node_a)
            g.nodes.add(node_b)
            node_a = node_b
        return g

    def get_edges(self) -> Iterable[FrozenSet[Node]]:
        pairs = set()
        for n in self.nodes:
            for e in n.edges:
                pairs.add(frozenset({n, e}))
        return iter(pairs)

    def to_nx(self):
        g = nx.Graph()
        g.add_nodes_from(iter(self.nodes))
        g.add_edges_from(self.get_edges())
        return g

    def draw(self, **draw_kwargs):
        g = self.to_nx()
        nx.draw(g, pos={n: n.point for n in iter(self.nodes)}, **draw_kwargs)


class SvgGraph(Graph):
    # TODO: fix orientation of SVG axes relative to graph/matplotlib axes
    # TODO: reorganize these classes to make it a little more object-oriented

    @classmethod
    def from_svg(cls, svgfile: str, resolution: int = 100):
        paths, attributes = svg2paths(svgfile)
        #  now use methods provided by the path_data object
        #  e.g. points can be extracted using
        #  point = path_data.pos(pos_val)
        #  where pos_val is anything between 0 and 1
        return cls.from_paths(
            list(map(
                lambda a: (a.real, a.imag),
                (p.point(t) for t in np.linspace(0, 1, resolution))))
            for p in paths)


if __name__ == '__main__':
    d = [
        [(0, 0), (1, 1)],  # simple two-point line
        [(0, 0), (0, 1), (1, 2), (2, 3), (0, 0)],  # a cycle
        [(1, 2), (4, 5), (2, 3)],  # a bent three-point line
    ]
    g = Graph.from_drawing(d)
    g2 = SvgGraph.from_svg('test.svg')
