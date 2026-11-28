"""Undirected graph stored as an adjacency matrix, with bidirectional iterators."""

from typing import Any, Callable, Generic, Iterator, List, NamedTuple, Optional, TypeVar

T = TypeVar("T")
Item = TypeVar("Item")

EDGE_COUNTED_AT_BOTH_ENDS = 2


class GraphError(Exception):
    """Raised for invalid graph operations."""


class Vertex(Generic[T]):
    """Handle of a graph vertex holding a value."""

    __slots__ = ("value",)

    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Vertex({self.value!r})"


class ConstVertex(Generic[T]):
    """Read-only view of a vertex, produced by const iterators."""

    __slots__ = ("_vertex",)

    def __init__(self, vertex: Vertex) -> None:
        self._vertex = vertex

    @property
    def value(self) -> T:
        return self._vertex.value

    def __repr__(self) -> str:
        return f"ConstVertex({self.value!r})"


class Edge(NamedTuple):
    """An edge as a pair of vertices."""

    first: Any
    second: Any


class BidirectionalIterator(Generic[Item]):
    """Iterator that can move forward (next) and backward (prev) over a snapshot of items."""

    def __init__(self, items: list, wrap: Callable = lambda item: item, reverse: bool = False, read_only: bool = False):
        self._items = items[::-1] if reverse else list(items)
        self._wrap = wrap
        self._position = 0
        self._last_index: Optional[int] = None
        self.read_only = read_only

    def __iter__(self) -> "BidirectionalIterator[Item]":
        return self

    def __next__(self) -> Item:
        if self._position >= len(self._items):
            raise StopIteration
        self._last_index = self._position
        self._position += 1
        return self._wrap(self._items[self._last_index])

    def prev(self) -> Item:
        """Step back and return the element that was passed over."""
        if self._position <= 0:
            raise StopIteration
        self._position -= 1
        self._last_index = self._position
        return self._wrap(self._items[self._last_index])

    def current_raw(self) -> Any:
        """Return the unwrapped element most recently returned by next/prev."""
        if self._last_index is None:
            raise GraphError("Iterator does not point to an element")
        return self._items[self._last_index]


class Graph(Generic[T]):
    """Undirected graph without self-loops; a vertex stores a value of type T.

    Equality compares values and edges; ordering compares (vertex count, edge count).
    """

    value_type = T
    Vertex = Vertex
    Edge = Edge

    def __init__(self) -> None:
        self._vertices: List[Vertex] = []
        self._matrix: List[List[bool]] = []

    def copy(self) -> "Graph[T]":
        """Return a deep copy (new vertex handles, same values and edges)."""
        clone: Graph[T] = Graph()
        clone.assign_from(self)
        return clone

    def assign_from(self, other: "Graph[T]") -> None:
        """Replace the state of this graph with a copy of the other graph."""
        if other is self:
            return
        self._vertices = [Vertex(vertex.value) for vertex in other._vertices]
        self._matrix = [row[:] for row in other._matrix]

    def empty(self) -> bool:
        return not self._vertices

    def clear(self) -> None:
        self._vertices = []
        self._matrix = []

    def _index(self, vertex: Any) -> int:
        for index, candidate in enumerate(self._vertices):
            if candidate is vertex:
                return index
        raise GraphError(f"Vertex {vertex!r} is not in the graph")

    def _edge_indexes(self, first: Vertex, second: Vertex) -> tuple:
        return self._index(first), self._index(second)

    def has_vertex(self, vertex: Any) -> bool:
        return any(candidate is vertex for candidate in self._vertices)

    def has_edge(self, first: Vertex, second: Vertex) -> bool:
        row, column = self._edge_indexes(first, second)
        return self._matrix[row][column]

    def vertex_count(self) -> int:
        return len(self._vertices)

    def edge_count(self) -> int:
        return len(self._edges())

    def degree(self, vertex: Vertex) -> int:
        """Number of edges touching the vertex."""
        return sum(self._matrix[self._index(vertex)])

    def edge_degree(self, first: Vertex, second: Vertex) -> int:
        """Number of other edges sharing an endpoint with the given edge."""
        if not self.has_edge(first, second):
            raise GraphError("Edge is not in the graph")
        return self.degree(first) + self.degree(second) - EDGE_COUNTED_AT_BOTH_ENDS

    def add_vertex(self, value: T) -> Vertex:
        for row in self._matrix:
            row.append(False)
        self._vertices.append(Vertex(value))
        self._matrix.append([False] * len(self._vertices))
        return self._vertices[-1]

    def add_edge(self, first: Vertex, second: Vertex) -> None:
        row, column = self._edge_indexes(first, second)
        if row == column:
            raise GraphError("Self-loops are not supported")
        self._matrix[row][column] = self._matrix[column][row] = True

    def remove_vertex(self, vertex: Vertex) -> None:
        index = self._index(vertex)
        del self._vertices[index]
        del self._matrix[index]
        for row in self._matrix:
            del row[index]

    def remove_edge(self, first: Vertex, second: Vertex) -> None:
        if not self.has_edge(first, second):
            raise GraphError("Edge is not in the graph")
        row, column = self._edge_indexes(first, second)
        self._matrix[row][column] = self._matrix[column][row] = False

    def _edges(self) -> List[Edge]:
        count = len(self._vertices)
        return [
            Edge(self._vertices[row], self._vertices[column])
            for row in range(count)
            for column in range(row + 1, count)
            if self._matrix[row][column]
        ]

    def _incident_edges(self, vertex: Vertex) -> List[Edge]:
        return [edge for edge in self._edges() if vertex in edge]

    def _adjacent_vertices(self, vertex: Vertex) -> List[Vertex]:
        row = self._matrix[self._index(vertex)]
        return [self._vertices[column] for column, linked in enumerate(row) if linked]

    @staticmethod
    def _const_edge(edge: Edge) -> Edge:
        return Edge(ConstVertex(edge.first), ConstVertex(edge.second))

    def vertex_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._vertices)

    def reverse_vertex_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._vertices, reverse=True)

    def const_vertex_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._vertices, ConstVertex, read_only=True)

    def const_reverse_vertex_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._vertices, ConstVertex, reverse=True, read_only=True)

    def edge_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._edges())

    def reverse_edge_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._edges(), reverse=True)

    def const_edge_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._edges(), self._const_edge, read_only=True)

    def const_reverse_edge_iterator(self) -> BidirectionalIterator:
        return BidirectionalIterator(self._edges(), self._const_edge, reverse=True, read_only=True)

    def incident_edge_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._incident_edges(vertex))

    def reverse_incident_edge_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._incident_edges(vertex), reverse=True)

    def const_incident_edge_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._incident_edges(vertex), self._const_edge, read_only=True)

    def const_reverse_incident_edge_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._incident_edges(vertex), self._const_edge, reverse=True, read_only=True)

    def adjacent_vertex_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._adjacent_vertices(vertex))

    def reverse_adjacent_vertex_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._adjacent_vertices(vertex), reverse=True)

    def const_adjacent_vertex_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._adjacent_vertices(vertex), ConstVertex, read_only=True)

    def const_reverse_adjacent_vertex_iterator(self, vertex: Vertex) -> BidirectionalIterator:
        return BidirectionalIterator(self._adjacent_vertices(vertex), ConstVertex, reverse=True, read_only=True)

    @staticmethod
    def _target(iterator: BidirectionalIterator, expected_type: type) -> Any:
        if iterator.read_only:
            raise GraphError("Cannot modify the graph through a const iterator")
        target = iterator.current_raw()
        if not isinstance(target, expected_type):
            raise GraphError(f"Iterator does not point to a {expected_type.__name__}")
        return target

    def erase_vertex(self, iterator: BidirectionalIterator) -> None:
        """Remove the vertex the iterator currently points to."""
        self.remove_vertex(self._target(iterator, Vertex))

    def erase_edge(self, iterator: BidirectionalIterator) -> None:
        """Remove the edge the iterator currently points to."""
        edge = self._target(iterator, Edge)
        self.remove_edge(edge.first, edge.second)

    def __iter__(self) -> Iterator[Vertex]:
        return self.vertex_iterator()

    def _state(self) -> tuple:
        return [vertex.value for vertex in self._vertices], self._matrix

    def _size(self) -> tuple:
        return self.vertex_count(), self.edge_count()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph):
            return NotImplemented
        return self._state() == other._state()

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        return result if result is NotImplemented else not result

    def _compare_sizes(self, other: object, compare: Callable[[tuple, tuple], bool]) -> bool:
        if not isinstance(other, Graph):
            return NotImplemented
        return compare(self._size(), other._size())

    def __lt__(self, other: object) -> bool:
        return self._compare_sizes(other, lambda mine, theirs: mine < theirs)

    def __gt__(self, other: object) -> bool:
        return self._compare_sizes(other, lambda mine, theirs: mine > theirs)

    def __le__(self, other: object) -> bool:
        return self._compare_sizes(other, lambda mine, theirs: mine <= theirs)

    def __ge__(self, other: object) -> bool:
        return self._compare_sizes(other, lambda mine, theirs: mine >= theirs)

    __hash__ = None  # type: ignore[assignment]

    def __str__(self) -> str:
        vertices = ", ".join(str(vertex.value) for vertex in self.const_vertex_iterator())
        edges = ", ".join(f"{edge.first.value}-{edge.second.value}" for edge in self.const_edge_iterator())
        return f"Graph(vertices=[{vertices}], edges=[{edges}])"
