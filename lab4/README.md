# Lab 4: Generic programming — sorting and containers (Python)

## Contents
- `generic_lab/sorting.py` — `bubble_sort` and `patience_sort`: in-place, work on any mutable sequence
  (`list`, `array.array`, ...) of any comparable type, with optional `key` and `reverse`.
- `generic_lab/models.py` — `Student`, a custom class used to demo sorting of user-defined objects.
- `generic_lab/graph.py` — `Graph[T]`: undirected graph stored as an adjacency matrix. The internal
  representation is hidden; access goes through methods and iterators only.
- `generic_lab/cli.py`, `main.py` — console menu demonstrating both parts.

## Graph API
- Vertices are opaque `Vertex` handles holding a value; edges are `Edge(first, second)` tuples. Self-loops are rejected.
- Queries: `has_vertex`, `has_edge`, `vertex_count`, `edge_count`, `degree`, `edge_degree`
  (number of other edges sharing an endpoint), `empty`.
- Modification: `add_vertex`, `add_edge`, `remove_vertex`, `remove_edge`, `erase_vertex(it)`, `erase_edge(it)`, `clear`.
- Copying: `copy()` (deep copy) and `assign_from(other)`.
- Comparison: `==`/`!=` compare values and edges; `<`, `>`, `<=`, `>=` compare (vertex count, edge count).
- Bidirectional iterators (`next` via `for`/`next()`, `prev()`) for vertices, edges, incident edges and adjacent
  vertices, each in four flavours: `X_iterator`, `reverse_X_iterator`, `const_X_iterator`, `const_reverse_X_iterator`.
  Const iterators yield read-only views and cannot be used to erase.
- Errors raise `GraphError`; `str(graph)` is built with the const iterators.

## Run
```bash
python main.py
```

## Development
```bash
pip install -r requirements-dev.txt
black --check .
flake8            # max cyclomatic complexity is 4
pytest            # fails if coverage is below 90%
```

CI (`.github/workflows/lab4.yaml`) runs Black, Flake8 and the tests on Python 3.10–3.13.
