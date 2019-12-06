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
Path = Iterable[Point]

Drawing = Iterable[Path]


def pairwise(iterable):
    """Return overlapping pairs of an iterable.

    s -> (s0,s1), (s1,s2), (s2, s3), ...

    From <https://docs.python.org/3/library/itertools.html#itertools-recipes>.
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


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

    def walk(self, start: 'Node' = None):
        """Generator that walks along nodes connected in a path."""
        if start is None:
            if len(self.edges) > 1:
                raise ValueError('Node {!r} has more than one edge'.format(self))
            if len(self.edges) == 0:
                return
            start = next(iter(self.edges))
        yield self
        if len(start.edges) > 2:
            raise ValueError('Next node {!r} has more than two edges'.format(start))
        try:
            next_node = next(iter(start.edges.difference({self})))
        except StopIteration:
            # next node has no other edges
            yield start
        else:
            yield from start.walk(next_node)
        return

    def path_length(self, start: 'Node' = None) -> float:
        """Get the length of a path from the node, optionally specified with a direction."""
        # here the path is walked and successive pairs of connected nodes are
        # fed into the `dist` function
        # For a path of nodes n1->n2->n3->n4 (where start=n1), this is
        # equivalent to sum([dist(n1, n2), dist(n2, n3), dist(n3, n4)])
        return sum(itertools.starmap(dist, pairwise(self.walk(start=start))))


class Graph(object):
    """A collection of interlinked Nodes."""

    def __init__(self):
        self.nodes = set()

    def get_edges(self) -> Iterable[FrozenSet[Node]]:
        """Get an iterable of all edges in the graph."""
        pairs = set()
        for n in self.nodes:
            for e in n.edges:
                pairs.add(frozenset({n, e}))
        return iter(pairs)

    def to_nx(self):
        """Make a NetworkX-compatible graph."""
        g = nx.Graph()
        g.add_nodes_from(iter(self.nodes))
        g.add_edges_from(self.get_edges())
        return g

    def draw(self, **draw_kwargs):
        """Draw the graph using matplotlib/networkx."""
        g = self.to_nx()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if 'pos' not in draw_kwargs:
            draw_kwargs['pos'] = {n: n.point for n in iter(self.nodes)}
        nx.draw(g, ax=ax, **draw_kwargs)
        ax.set_aspect('equal')

    def validate_path(self, start: Node):
        """Assert that the path beginning with `start` reaches all nodes in the graph."""
        nodes_in_path = set(start.walk())
        assert nodes_in_path == self.nodes, "Path does not contain all nodes"

    def add_from_path(self, p: Path):
        """Add a path of connected nodes from a series of points."""
        # iterate through points from path, adding nodes while connecting the
        # previous node to the current
        p = iter(p)
        node_a = Node(next(p))
        start = node_a
        self.nodes.add(node_a)
        for point in p:
            node_b = Node(point)
            node_b.connect(node_a)
            self.nodes.add(node_b)
            node_a = node_b
        end = node_b
        return (start, end)

    def add_from_paths(self, ps: Iterable[Path]):
        """Add multiple distinct paths to the graph."""
        for path in ps:
            self.add_from_path(path)


class SvgGraph(Graph):
    """Graph of distinct paths loaded from an svg."""

    def __init__(self, svgfile: str, resolution: int = 100):
        super().__init__()
        paths, attributes = svg2paths(svgfile)
        #  now use methods provided by the path_data object
        #  e.g. points can be extracted using
        #  point = path_data.pos(pos_val)
        #  where pos_val is anything between 0 and 1
        self.add_from_paths(self._svgpath_to_points(p) for p in paths)

    @staticmethod
    def _svgpath_to_points(path, resolution: int = 100):
        """Convert svg.path's path objects to a point-tuple iterator."""
        return map(
            lambda a: (a.real, a.imag),
            (path.point(t) for t in np.linspace(0, 1, resolution)))

    def draw(self, **draw_kwargs):
        # flip y-coordinates to reconcile svg and matplotlib axes
        super().draw(g, pos={n: (n.point[0], -n.point[1]) for n in iter(self.nodes)}, **draw_kwargs)


class NaiveSvgGraph(SvgGraph):
    """A graph of a single path built from an svg, connecting subsequent paths.

    This represents the path created by parsing an svg in-place with no sorting.

    The start node of this path is stored as `self.start` after initialization.
    """

    def __init__(self, svgfile: str, resolution: int = 100):
        Graph.__init__(self)
        paths, attributes = svg2paths(svgfile)
        # rather than add a new path for each svgpath, chain the svgpath points
        # together for a single path
        point_iterator = itertools.chain.from_iterable(
            self._svgpath_to_points(p) for p in paths)
        (self.start, _) = self.add_from_path(point_iterator)


if __name__ == '__main__':
    d = [
        [(0, 0), (1, 1)],  # simple two-point line
        [(0, 0), (0, 1), (1, 2), (2, 3), (0, 0)],  # a cycle
        [(1, 2), (4, 5), (2, 3)],  # a bent three-point line
    ]
    g = Graph()
    g.add_from_paths(d)
    g2 = SvgGraph('test.svg')
