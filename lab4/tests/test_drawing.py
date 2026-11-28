from generic_lab import Graph
from generic_lab.drawing import draw_graph, line_char, line_points, node_positions


def build(edge_pairs, count):
    graph = Graph()
    vertices = [graph.add_vertex(index) for index in range(count)]
    for first, second in edge_pairs:
        graph.add_edge(vertices[first], vertices[second])
    return graph


def test_empty_graph_draws_nothing():
    assert draw_graph(Graph()) == ""


def test_vertices_are_labelled_and_edges_drawn():
    picture = draw_graph(build([(0, 1), (1, 2), (2, 3), (3, 0)], 4))
    assert all(f"({number})" in picture for number in range(1, 5))
    assert any(char in picture for char in "-|/\\")


def test_no_edges_means_no_lines():
    picture = draw_graph(build([], 3))
    assert not any(char in picture for char in "-|/\\")


def test_line_characters():
    assert line_char((0, 0), (10, 0)) == "-"
    assert line_char((0, 0), (0, 10)) == "|"
    assert line_char((0, 0), (5, 5)) == "\\"
    assert line_char((0, 5), (5, 0)) == "/"


def test_geometry_helpers():
    assert line_points((0, 0), (0, 0)) == [(0, 0), (0, 0)]
    assert line_points((0, 0), (2, 0)) == [(0, 0), (1, 0), (2, 0)]
    assert len(set(node_positions(6))) == 6
