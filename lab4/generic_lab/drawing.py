"""Plain-text drawing of a graph: vertices on a circle, edges as lines of characters."""

import math
from itertools import combinations
from typing import List, Tuple

from .graph import Graph

CANVAS_WIDTH = 61
CANVAS_HEIGHT = 21
HORIZONTAL_RADIUS = (CANVAS_WIDTH - 9) // 2
VERTICAL_RADIUS = (CANVAS_HEIGHT - 3) // 2
STEEP_RATIO = 2
Point = Tuple[int, int]


def node_positions(count: int) -> List[Point]:
    """Evenly spread vertex centres over an ellipse, the first vertex at the top."""
    centre_column, centre_row = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
    angles = [2 * math.pi * index / count - math.pi / 2 for index in range(count)]
    return [
        (
            round(centre_column + HORIZONTAL_RADIUS * math.cos(angle)),
            round(centre_row + VERTICAL_RADIUS * math.sin(angle)),
        )
        for angle in angles
    ]


def line_points(start: Point, end: Point) -> List[Point]:
    steps = max(abs(end[0] - start[0]), abs(end[1] - start[1]), 1)
    delta_column, delta_row = end[0] - start[0], end[1] - start[1]
    return [
        (round(start[0] + delta_column * step / steps), round(start[1] + delta_row * step / steps))
        for step in range(steps + 1)
    ]


def line_char(start: Point, end: Point) -> str:
    delta_column, delta_row = abs(end[0] - start[0]), abs(end[1] - start[1])
    if delta_column > STEEP_RATIO * delta_row:
        return "-"
    if delta_row > STEEP_RATIO * delta_column:
        return "|"
    return "/" if (end[0] - start[0]) * (end[1] - start[1]) < 0 else "\\"


def put_text(canvas: List[List[str]], centre: Point, text: str) -> None:
    first_column = centre[0] - len(text) // 2
    for offset, char in enumerate(text):
        canvas[centre[1]][first_column + offset] = char


def draw_line(canvas: List[List[str]], start: Point, end: Point) -> None:
    char = line_char(start, end)
    for column, row in line_points(start, end):
        canvas[row][column] = char


def draw_edges(canvas: List[List[str]], graph: Graph, vertices: list, positions: List[Point]) -> None:
    for first, second in combinations(range(len(vertices)), 2):
        if graph.has_edge(vertices[first], vertices[second]):
            draw_line(canvas, positions[first], positions[second])


def draw_graph(graph: Graph) -> str:
    """Return the picture of the graph; vertices are labelled with their 1-based numbers."""
    vertices = list(graph.vertex_iterator())
    if not vertices:
        return ""
    canvas = [[" "] * CANVAS_WIDTH for _ in range(CANVAS_HEIGHT)]
    positions = node_positions(len(vertices))
    draw_edges(canvas, graph, vertices, positions)
    for number, position in enumerate(positions, 1):
        put_text(canvas, position, f"({number})")
    return "\n".join("".join(row).rstrip() for row in canvas).strip("\n")
