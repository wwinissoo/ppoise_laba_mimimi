"""Implementation of the Tic-Tac-Toe game class."""

class TicTacToe():
    """
    Tic-Tac-Toe game for two players.

    The board is square and has a size of at least 3.
    Players use the X and O marks.
    """
    __hash__ = None
    """Mutable game objects are intentionally unhashable."""

    def __init__(self, size):
        """
        Create an empty size-by-size board, where size is at least 3.

        If another TicTacToe object is passed, create a copy of it.

        :param size: Board size (integer >= 3) or another TicTacToe object.
        :raises ValueError: If the board size is invalid.
        """
        if isinstance(size, TicTacToe):
            self.__size = size.__size
            self.__board = [line[:] for line in size.__board]
            return

        if not isinstance(size, int) or isinstance(size, bool) or size < 3:
            raise ValueError("Board size must be an integer of at least 3.")

        self.__size = size
        self.__board = [[" "] * size for _ in range(size)]

    def get_size(self):
        """Return the board size."""
        return self.__size

    def _check_position(self, position):
        """Validate a (row, column) position."""
        if not isinstance(position, tuple) or len(position) != 2:
            raise TypeError("Position must be a (row, column) tuple.")

        row = position[0]
        col = position[1]

        if not isinstance(row, int) or isinstance(row, bool):
            raise TypeError("Row index must be an integer.")

        if not isinstance(col, int) or isinstance(col, bool):
            raise TypeError("Column index must be an integer.")

        if row < 0 or row >= self.__size:
            raise IndexError("Row index is outside the board.")

        if col < 0 or col >= self.__size:
            raise IndexError("Column index is outside the board.")

    def can_set(self, position, value):
        """
        Check whether X or O can be placed at a position.

        :param position: (row, column) tuple, zero-based.
        :param value: "X" or "O".
        :return: True if the cell is empty and the mark is valid.
        :raises TypeError: If the position is invalid.
        :raises IndexError: If the position is outside the board.
        """
        self._check_position(position)

        if value != "X" and value != "O":
            return False

        row = position[0]
        col = position[1]

        if self.__board[row][col] == " ":
            return True

        return False

    def __getitem__(self, position):
        """
        Return a cell value using `game[row, col]`.

        :return: "X", "O", or " " (an empty cell).
        :raises TypeError: If the position is invalid.
        :raises IndexError: If the position is outside the board.
        """
        self._check_position(position)
        return self.__board[position[0]][position[1]]

    def __setitem__(self, position, value):
        """
        Set X or O in a cell using `game[row, col] = "X"`.

        :raises ValueError: If the mark is invalid or the cell is occupied.
        :raises TypeError: If the position is invalid.
        :raises IndexError: If the position is outside the board.
        """
        self._check_position(position)

        if value != "X" and value != "O":
            raise ValueError("Only X or O can be placed.")

        row = position[0]
        col = position[1]

        if self.__board[row][col] != " ":
            raise ValueError("Cell is already occupied.")

        self.__board[row][col] = value

    def _winner_on_line(self, positions):
        """Return the mark if every position in a line contains it."""
        positions = iter(positions)
        row, col = next(positions)
        mark = self.__board[row][col]

        if mark == " ":
            return None

        if all(self.__board[row][col] == mark for row, col in positions):
            return mark
        return None

    def _winner_in_rows(self):
        """Return the winner found in any row, if one exists."""
        for row in range(self.__size):
            winner = self._winner_on_line(
                (row, col) for col in range(self.__size)
            )
            if winner is not None:
                return winner
        return None

    def _winner_in_columns(self):
        """Return the winner found in any column, if one exists."""
        for col in range(self.__size):
            winner = self._winner_on_line(
                (row, col) for row in range(self.__size)
            )
            if winner is not None:
                return winner
        return None

    def _winner_in_diagonals(self):
        """Return the winner found in either diagonal, if one exists."""
        main_diagonal = self._winner_on_line(
            (index, index) for index in range(self.__size)
        )
        if main_diagonal is not None:
            return main_diagonal

        return self._winner_on_line(
            (index, self.__size - 1 - index)
            for index in range(self.__size)
        )

    def winner(self):
        """Check rows, columns, and diagonals for a winner."""
        for check_lines in (
            self._winner_in_rows,
            self._winner_in_columns,
            self._winner_in_diagonals,
        ):
            winner = check_lines()
            if winner is not None:
                return winner
        return None

    def is_full(self):
        """Return whether the board is full."""
        for row in range(self.__size):
            for col in range(self.__size):
                if self.__board[row][col] == " ":
                    return False
        return True

    def __eq__(self, other):
        """Compare two game boards for equality."""
        if not isinstance(other, TicTacToe):
            return False

        return self.__size == other.__size and self.__board == other.__board

    def __ne__(self, other):
        """Compare two game boards for inequality."""
        return not self == other

    def __str__(self):
        """Return a human-readable representation of the board."""
        lines = []
        for row in range(self.__size):
            lines.append(" | ".join(self.__board[row]))
        return "\n".join(lines)

    def __repr__(self):
        """Return a string that can recreate this object."""
        return f"TicTacToe.from_text({self.to_text()!r})"

    def to_text(self):
        """Serialize the board as text."""
        lines = []
        for row in range(self.__size):
            line = []
            for col in range(self.__size):
                value = self.__board[row][col]
                if value == " ":
                    value = "-"
                line.append(value)
            lines.append(" ".join(line))
        return "\n".join(lines)

    @classmethod
    def from_text(cls, text):
        """Create a game board from text."""
        lines = text.strip().splitlines()

        if len(lines) == 0:
            raise ValueError("Board text is empty.")

        rows = []
        for line in lines:
            rows.append(line.split())

        size = len(rows)

        for row in rows:
            if len(row) != size:
                raise ValueError("Board must be square.")

        game = cls(size)

        for row in range(size):
            for col in range(size):
                value = rows[row][col]

                if value != "-" and value != "X" and value != "O":
                    raise ValueError("Only X, O, and - are allowed.")

                if value != "-":
                    game[row, col] = value

        return game

    @classmethod
    def from_string(cls, text):
        """Alias for `from_text`."""
        return cls.from_text(text)

    def write(self, stream):
        """
        Write the board to a text stream (file, io.StringIO, sys.stdout).

        :param stream: An object with a write() method.
        """
        stream.write(self.to_text() + "\n")

    @classmethod
    def read(cls, stream):
        """
        Read a board from a text stream.

        :param stream: An object with a read() method.
        :return: A new TicTacToe object.
        :raises ValueError: If the stream contains invalid data.
        """
        return cls.from_text(stream.read())

    def copy(self):
        """Create an independent copy of the board."""
        return TicTacToe(self)

    def assign(self, other):
        """
        Copy the state of other into this board.

        :param other: Another TicTacToe object.
        :return: self, allowing method chaining.
        :raises TypeError: If other is not a TicTacToe object.
        """
        if not isinstance(other, TicTacToe):
            raise TypeError("Only a TicTacToe object can be assigned.")

        if other is not self:
            self.__size = other.__size
            self.__board = [line[:] for line in other.__board]

        return self

    def __copy__(self):
        """Support copy.copy()."""
        return self.copy()

    def __deepcopy__(self, memo):
        """Support copy.deepcopy()."""
        return self.copy()
