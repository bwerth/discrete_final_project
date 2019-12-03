import abc
from typing import Tuple, List, Set


# type definitions
Point = Tuple[float, float]
Path = List[Point]

Drawing = List[Path]

Graph: Set[Node]


class Solvable(abc.ABC):
    def distance_to(self, other):
        pass


class Node(Solvable):
    def __init__(self, *points):
        self.points = list(*points)
        self.edges = set()

    def distance_to(self, other: Path):
        # TODO: look into <https://docs.python.org/3/library/functools.html#functools.lru_cache>
        # for this
        return tuple(abs(v1 - v2) for v1, v2 in zip(self.end, other.start))

    def distance_from(self, other: Path):
        return tuple(abs(v1 - v2) for v1, v2 in zip(other.end, self.start))

    def connect(self, other: Path):
        self.edges.add(self)
        other.edges.add(self)

    def is_connected(self, other: Path):
        assert (other in self.edges) == (self in other.edges)
        return self in other.edges

    @property
    def start(self):
        return self.points[0]

    @property
    def end(self):
        return self.points[-1]

    def __str__(self):
        return str(self.points)


def dist(one: Solvable, other: Solvable) -> float:
    return one.distance_to(other)
