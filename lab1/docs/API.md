# Lab 1: interface reference ("header" documentation)

Lab 1 is written in Python, which has no header files. This document plays the role of
the headers: for every module it lists the **public interface** (declarations only, no
implementation) with the contract of each member: parameters, result and raised exceptions.
Names with a leading underscore are private and are not part of the interface.

The generated pdoc documentation is in `docs/html/index.html` (rebuild with `pdoc -o docs/html Laba1_Vector/vector.py TicTacToe/game.py`).

---

## Module `Laba1_Vector/vector.py`

```python
def _is_number(value) -> bool                       # private helper

class Vector:
    def __init__(self, start, end)

    def get_start(self) -> tuple
    def get_end(self) -> tuple
    def get_x(self) -> number
    def get_y(self) -> number
    def get_z(self) -> number
    def length(self) -> float
    def cosine(self, other) -> float

    def __add__(self, other) -> Vector      def __iadd__(self, other) -> Vector
    def __sub__(self, other) -> Vector      def __isub__(self, other) -> Vector
    def __mul__(self, other) -> Vector      def __rmul__(self, number) -> Vector
    def __imul__(self, other) -> Vector
    def __truediv__(self, number) -> Vector def __itruediv__(self, number) -> Vector

    def __eq__(self, other) -> bool         def __ne__(self, other) -> bool
    def __lt__(self, other) -> bool         def __le__(self, other) -> bool
    def __gt__(self, other) -> bool         def __ge__(self, other) -> bool
    def __hash__(self) -> int

    def __str__(self) -> str                def __repr__(self) -> str
    def to_string(self) -> str
    @classmethod
    def from_string(cls, text) -> Vector
    def copy(self) -> Vector
```

### Contract

A `Vector` is a three-dimensional vector defined by a start point and an end point.
The state is private: `__start` and `__end`, each a tuple of three numbers.

| Member | Contract |
|---|---|
| `Vector(start, end)` | Two points of three coordinates each. Raises `ValueError` if a point does not have exactly three coordinates, `TypeError` if a coordinate is not a number (`bool` is not accepted). |
| `get_start()`, `get_end()` | Coordinates of the start and of the end point. |
| `get_x()`, `get_y()`, `get_z()` | Vector components: end minus start along the given axis. |
| `length()` | Euclidean length of the vector. |
| `cosine(other)` | Cosine of the angle between two vectors. `TypeError` if `other` is not a `Vector`, `ValueError` for a zero vector. |
| `+`, `+=`, `-`, `-=` | Component-wise addition and subtraction of two vectors; the augmented forms modify the object in place and return it. |
| `*` | Cross product when `other` is a `Vector`, multiplication by a number otherwise; `number * vector` works through `__rmul__`. |
| `/`, `/=` | Division by a number; dividing by zero raises `ZeroDivisionError`. |
| `==`, `!=` | Equality of vectors. |
| `<`, `<=`, `>`, `>=` | Comparison by length (`<` means "shorter than"). |
| `hash()` | Computed from the components; equal vectors have equal hashes. In-place operators change the hash, so do not mutate a vector used as a dictionary key. |
| `str()`, `repr()` | Human-readable and re-creatable representations. |
| `to_string()` | Text `"x1 y1 z1 x2 y2 z2"`. |
| `Vector.from_string(text)` | Builds a vector from such a string. `ValueError` if the count of numbers is not six or a value is not numeric. |
| `copy()` | An independent copy. |

---

## Module `TicTacToe/game.py`

```python
class TicTacToe:
    __hash__ = None                                 # boards are mutable, hence unhashable

    def __init__(self, size)                        # size: int >= 3, or another TicTacToe to copy

    def get_size(self) -> int
    def can_set(self, position, value) -> bool
    def __getitem__(self, position) -> str          # game[row, col]
    def __setitem__(self, position, value) -> None  # game[row, col] = "X"
    def winner(self) -> str | None
    def is_full(self) -> bool

    def __eq__(self, other) -> bool
    def __ne__(self, other) -> bool
    def __str__(self) -> str
    def __repr__(self) -> str

    def to_text(self) -> str
    @classmethod
    def from_text(cls, text) -> TicTacToe
    @classmethod
    def from_string(cls, text) -> TicTacToe         # alias of from_text
    def write(self, stream) -> None
    @classmethod
    def read(cls, stream) -> TicTacToe

    def copy(self) -> TicTacToe
    def assign(self, other) -> TicTacToe            # returns self, so calls can be chained
    def __copy__(self) -> TicTacToe
    def __deepcopy__(self, memo) -> TicTacToe
```

Private helpers (not part of the interface): `_check_position`, `_winner_on_line`,
`_winner_in_rows`, `_winner_in_columns`, `_winner_in_diagonals`.

### Contract

A square board of `size x size` cells. A cell holds `"X"`, `"O"` or `" "` (empty).
Positions are zero-based `(row, column)` tuples.

| Member | Contract |
|---|---|
| `TicTacToe(size)` | `size` must be an integer of at least 3, otherwise `ValueError`. Passing another `TicTacToe` creates a copy of it. |
| `get_size()` | Board side length. |
| `can_set(position, value)` | `True` if the mark is `"X"`/`"O"` and the cell is empty. `TypeError` for a malformed position, `IndexError` for a position outside the board. |
| `game[row, col]` | Returns `"X"`, `"O"` or `" "`. `TypeError` / `IndexError` as above. |
| `game[row, col] = mark` | Places a mark. `ValueError` if the mark is invalid or the cell is occupied. |
| `winner()` | Mark that fills a whole row, column or diagonal, or `None`. |
| `is_full()` | `True` when no empty cell is left. |
| `==`, `!=` | Boards are equal when size and all cells are equal. |
| `str()`, `repr()` | Printable board; `repr` is a string that can re-create the object. |
| `to_text()` | Serialisation as text (empty cells written as `-`). |
| `from_text(text)` / `from_string(text)` | Parses such text. `ValueError` for empty text, a non-square board or characters other than `X`, `O`, `-`. |
| `write(stream)` / `read(stream)` | Write to / read from a text stream (file, `io.StringIO`, `sys.stdout`). |
| `copy()`, `copy.copy()`, `copy.deepcopy()` | Independent copies of the board. |
| `assign(other)` | Copies the state of `other` into this board and returns `self`. |

---

## Entry points and tests

| File | Role |
|---|---|
| `Laba1_Vector/main.py` | Console demo of the `Vector` class. |
| `TicTacToe/main.py` | Console game built on `TicTacToe`. |
| `Laba1_Vector/test.py`, `TicTacToe/test_game.py` | Unit tests (`pytest`). |
