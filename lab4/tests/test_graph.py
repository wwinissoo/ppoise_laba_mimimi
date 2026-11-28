import pytest

from generic_lab import Graph, GraphError


@pytest.fixture
def triangle():
    graph = Graph()
    a, b, c, d = (graph.add_vertex(name) for name in "abcd")
    graph.add_edge(a, b)
    graph.add_edge(b, c)
    graph.add_edge(c, a)
    return graph, a, b, c, d


def values(iterator):
    return [item.value for item in iterator]


def pairs(iterator):
    return [(e.first.value, e.second.value) for e in iterator]


def test_empty_clear_and_counts(triangle):
    graph, a, b, c, d = triangle
    assert not graph.empty() and Graph().empty()
    assert (graph.vertex_count(), graph.edge_count()) == (4, 3)
    graph.clear()
    assert graph.empty() and graph.edge_count() == 0


def test_membership_and_degrees(triangle):
    graph, a, b, c, d = triangle
    assert graph.has_vertex(a) and graph.has_edge(a, b) and not graph.has_edge(a, d)
    assert graph.degree(a) == 2 and graph.degree(d) == 0
    assert graph.edge_degree(a, b) == 2
    with pytest.raises(GraphError):
        graph.edge_degree(a, d)


def test_errors(triangle):
    graph, a, b, c, d = triangle
    with pytest.raises(GraphError):
        graph.add_edge(a, a)
    with pytest.raises(GraphError):
        graph.remove_edge(a, d)
    other = Graph().add_vertex("x")
    assert not graph.has_vertex(other)
    with pytest.raises(GraphError):
        graph.degree(other)


def test_remove_vertex_and_edge(triangle):
    graph, a, b, c, d = triangle
    graph.remove_edge(a, b)
    assert not graph.has_edge(b, a)
    graph.remove_vertex(c)
    assert (graph.vertex_count(), graph.edge_count()) == (3, 0)
    assert not graph.has_vertex(c)


def test_iterators(triangle):
    graph, a, b, c, d = triangle
    assert values(graph.vertex_iterator()) == list("abcd")
    assert values(graph.reverse_vertex_iterator()) == list("dcba")
    assert values(graph.const_vertex_iterator()) == list("abcd")
    assert values(graph.const_reverse_vertex_iterator()) == list("dcba")
    assert values(graph) == list("abcd")
    expected = [("a", "b"), ("a", "c"), ("b", "c")]
    assert pairs(graph.edge_iterator()) == expected
    assert pairs(graph.reverse_edge_iterator()) == expected[::-1]
    assert pairs(graph.const_edge_iterator()) == expected
    assert pairs(graph.const_reverse_edge_iterator()) == expected[::-1]
    assert pairs(graph.incident_edge_iterator(b)) == [("a", "b"), ("b", "c")]
    assert pairs(graph.reverse_incident_edge_iterator(b)) == [("b", "c"), ("a", "b")]
    assert pairs(graph.const_incident_edge_iterator(b)) == [("a", "b"), ("b", "c")]
    assert pairs(graph.const_reverse_incident_edge_iterator(b)) == [("b", "c"), ("a", "b")]
    assert values(graph.adjacent_vertex_iterator(b)) == ["a", "c"]
    assert values(graph.reverse_adjacent_vertex_iterator(b)) == ["c", "a"]
    assert values(graph.const_adjacent_vertex_iterator(b)) == ["a", "c"]
    assert values(graph.const_reverse_adjacent_vertex_iterator(b)) == ["c", "a"]


def test_iterator_moves_backward(triangle):
    graph = triangle[0]
    iterator = graph.vertex_iterator()
    with pytest.raises(StopIteration):
        iterator.prev()
    assert next(iterator).value == "a" and next(iterator).value == "b"
    assert iterator.prev().value == "b"
    assert iterator.prev().value == "a"


def test_erase_by_iterator(triangle):
    graph, a, b, c, d = triangle
    iterator = graph.vertex_iterator()
    next(iterator)
    graph.erase_vertex(iterator)
    assert not graph.has_vertex(a)
    edges = graph.edge_iterator()
    next(edges)
    graph.erase_edge(edges)
    assert graph.edge_count() == 0


def test_erase_errors(triangle):
    graph = triangle[0]
    with pytest.raises(GraphError):
        graph.erase_vertex(graph.vertex_iterator())
    const_iterator = graph.const_vertex_iterator()
    next(const_iterator)
    with pytest.raises(GraphError):
        graph.erase_vertex(const_iterator)
    edges = graph.edge_iterator()
    next(edges)
    with pytest.raises(GraphError):
        graph.erase_vertex(edges)


def test_copy_assign_and_comparison(triangle):
    graph = triangle[0]
    clone = graph.copy()
    assert clone == graph and not clone != graph and clone <= graph and clone >= graph
    assert not clone < graph and not clone > graph
    assert list(clone)[0] is not list(graph)[0]
    clone.add_vertex("e")
    assert clone != graph and clone > graph and graph < clone
    graph.assign_from(clone)
    graph.assign_from(graph)
    assert graph == clone
    other = Graph()
    other.assign_from(Graph())
    assert other.empty()


def test_comparison_with_other_types():
    graph = Graph()
    assert graph != 5 and not graph == 5
    with pytest.raises(TypeError):
        graph < 5


def test_str(triangle):
    assert str(triangle[0]) == "Graph(vertices=[a, b, c, d], edges=[a-b, a-c, b-c])"


def test_vertex_repr_and_value_change():
    graph = Graph()
    vertex = graph.add_vertex(1)
    view = next(graph.const_vertex_iterator())
    vertex.value = 2
    assert view.value == 2 and repr(vertex) == "Vertex(2)" and repr(view) == "ConstVertex(2)"
