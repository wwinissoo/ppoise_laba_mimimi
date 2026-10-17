import copy
import io

import pytest


import main as main
from game import TicTacToe

def test_create_board():
    game = TicTacToe(3)
    assert game.get_size() == 3
    assert game[0, 0] == " "


def test_wrong_size():
    for value in [0, -1, 1, 2, 3.5, True]:
        with pytest.raises(ValueError):
            TicTacToe(value)


def test_get_set_and_can_set():
    game = TicTacToe(3)
    assert game.can_set((0, 0), "X") is True
    game[0, 0] = "X"
    assert game[0, 0] == "X"
    assert game.can_set((0, 0), "O") is False


def test_wrong_value():
    game = TicTacToe(3)
    assert game.can_set((0, 0), "A") is False
    with pytest.raises(ValueError):
        game[0, 0] = "A"


def test_busy_cell():
    game = TicTacToe(3)
    game[0, 0] = "X"
    with pytest.raises(ValueError):
        game[0, 0] = "O"


def test_wrong_position():
    game = TicTacToe(3)
    for position in [(3, 0), (0, 3), (-1, 0)]:
        with pytest.raises(IndexError):
            game[position] = "X"

    for position in [0, (0,), ("0", 1), (0, "1")]:
        with pytest.raises(TypeError):
            game[position] = "X"


def test_can_set_wrong_position():
    game = TicTacToe(3)
    with pytest.raises(IndexError):
        game.can_set((3, 0), "X")


def test_row_winner_x():
    game = TicTacToe(3)
    for col in range(3):
        game[0, col] = "X"
    assert game.winner() == "X"


def test_row_winner_o():
    game = TicTacToe(3)
    for col in range(3):
        game[2, col] = "O"
    assert game.winner() == "O"


def test_row_not_winner():
    game = TicTacToe(3)
    game[0, 0] = "X"
    game[0, 1] = "O"
    game[0, 2] = "X"
    assert game.winner() is None


def test_column_winner():
    game = TicTacToe(3)
    for row in range(3):
        game[row, 1] = "X"
    assert game.winner() == "X"


def test_column_not_winner():
    game = TicTacToe(3)
    game[0, 1] = "X"
    game[1, 1] = "O"
    game[2, 1] = "X"
    assert game.winner() is None


def test_main_diagonal_winner():
    game = TicTacToe(3)
    for i in range(3):
        game[i, i] = "X"
    assert game.winner() == "X"


def test_main_diagonal_not_winner():
    game = TicTacToe(3)
    game[0, 0] = "X"
    game[1, 1] = "O"
    game[2, 2] = "X"
    assert game.winner() is None


def test_second_diagonal_winner():
    game = TicTacToe(3)
    for i in range(3):
        game[i, 2 - i] = "O"
    assert game.winner() == "O"


def test_second_diagonal_not_winner():
    game = TicTacToe(3)
    game[0, 2] = "O"
    game[1, 1] = "X"
    game[2, 0] = "O"
    assert game.winner() is None


def test_no_winner_empty():
    assert TicTacToe(3).winner() is None


def test_full_and_not_full():
    game = TicTacToe(3)
    assert game.is_full() is False
    for row in range(3):
        for col in range(3):
            game[row, col] = "X"
    assert game.is_full() is True


def test_equality():
    first = TicTacToe(3)
    second = TicTacToe(3)
    first[0, 0] = "X"
    second[0, 0] = "X"
    assert first == second
    assert not first != second


def test_inequality():
    first = TicTacToe(3)
    second = TicTacToe(3)
    first[0, 0] = "X"
    second[0, 0] = "O"
    assert first != second
    assert first != 5
    assert TicTacToe(3) != TicTacToe(4)


def test_string():
    game = TicTacToe(3)
    game[0, 0] = "X"
    game[1, 1] = "O"
    result = str(game)
    assert "X" in result
    assert "O" in result
    assert "|" in result


def test_to_text():
    game = TicTacToe(3)
    game[0, 0] = "X"
    game[2, 2] = "O"
    assert game.to_text() == "X - -\n- - -\n- - O"


def test_from_text():
    game = TicTacToe.from_text("X - -\n- - -\n- - O")
    assert game.get_size() == 3
    assert game[0, 0] == "X"
    assert game[0, 1] == " "
    assert game[2, 2] == "O"


def test_from_text_errors():
    with pytest.raises(ValueError):
        TicTacToe.from_text("")
    with pytest.raises(ValueError):
        TicTacToe.from_text("X -\n-")
    with pytest.raises(ValueError):
        TicTacToe.from_text("X A\n- O")


def test_copy():
    game = TicTacToe(3)
    game[0, 0] = "X"
    duplicate = game.copy()
    assert duplicate == game
    assert duplicate is not game
    duplicate[0, 1] = "O"
    assert game[0, 1] == " "


def test_copy_module():
    game = TicTacToe(3)
    game[0, 0] = "X"
    duplicate = copy.copy(game)
    assert duplicate == game
    assert duplicate is not game


def test_large_board():
    game = TicTacToe(5)
    for col in range(5):
        game[2, col] = "X"
    assert game.winner() == "X"


def test_board_size_one():
    with pytest.raises(ValueError):
        TicTacToe(1)


def test_copy_constructor():
    game = TicTacToe(3)
    game[1, 1] = "X"
    duplicate = TicTacToe(game)
    assert duplicate == game
    duplicate[0, 0] = "O"
    assert game[0, 0] == " "


def test_deepcopy():
    game = TicTacToe(3)
    game[0, 0] = "X"
    duplicate = copy.deepcopy(game)
    assert duplicate == game
    duplicate[0, 1] = "O"
    assert game != duplicate


def test_assign():
    first = TicTacToe(3)
    second = TicTacToe(4)
    second[3, 3] = "O"
    assert first.assign(second) is first
    assert first == second
    assert first.get_size() == 4
    second[0, 0] = "X"
    assert first[0, 0] == " "
    assert first.assign(first) is first
    with pytest.raises(TypeError):
        first.assign("not a game")


def test_unhashable():
    with pytest.raises(TypeError):
        hash(TicTacToe(3))


def test_repr_round_trip():
    game = TicTacToe(3)
    game[0, 1] = "X"
    assert eval(repr(game)) == game


def test_from_string():
    text = "X - -\n- - -\n- - O"
    assert TicTacToe.from_string(text) == TicTacToe.from_text(text)


def test_text_round_trip():
    game = TicTacToe(3)
    game[0, 0] = "X"
    game[2, 1] = "O"
    assert TicTacToe.from_text(game.to_text()) == game


def test_stream_round_trip():
    game = TicTacToe(3)
    game[1, 2] = "O"
    stream = io.StringIO()
    game.write(stream)
    stream.seek(0)
    assert TicTacToe.read(stream) == game


def test_file_round_trip(tmp_path):
    game = TicTacToe(4)
    game[3, 0] = "X"
    path = tmp_path / "board.txt"
    with open(path, "w", encoding="utf-8") as file:
        game.write(file)
    with open(path, encoding="utf-8") as file:
        assert TicTacToe.read(file) == game

def run_main(monkeypatch, capsys, answers):
    answers = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main.main()
    return capsys.readouterr().out
def test_main_exit(monkeypatch, capsys):
    out = run_main(monkeypatch, capsys, ["abc", "0", "3", "1", "0"])
    assert "Error" in out
    assert "Program finished." in out
def test_main_x_wins(monkeypatch, capsys):
    moves = ["1", "1", "2", "1", "1", "2", "2", "2", "1", "3"]
    answers = ["3"]
    for i in range(0, len(moves), 2):
        answers += ["2", moves[i], moves[i + 1]]
    answers += ["2", "3", "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "Player X wins!" in out
    assert "Game over" in out
    assert "Player X wins." in out

def test_main_rejects_small_size(monkeypatch, capsys):
    out = run_main(monkeypatch, capsys, ["2", "3", "0"])
    assert "at least 3" in out
    assert "Program finished." in out

def test_main_draw(monkeypatch, capsys):
    answers = ["3", "6", "X O X;X O O;O X -", "2", "3", "3", "4", "2", "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "Turn: player X" in out
    assert "Draw!" in out
    assert "The board is full." in out
    assert "Game over. Draw!" in out


def test_main_bad_moves(monkeypatch, capsys):
    answers = ["3", "2", "5", "1", "2", "a", "2", "1", "1", "2", "1", "1",
               "4", "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "outside the board" in out
    assert "invalid literal" in out
    assert "Cannot place a mark" in out
    assert "The board has empty cells." in out


def test_main_text_and_copy(monkeypatch, capsys):
    answers = ["3", "6", "X - -;- O -;- - -", "5", "7", "6",
               "X A -;- - -;- - -", "3", "99", "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "Board loaded." in out
    assert "X - -\n- O -\n- - -" in out
    assert "Copy equals original: True" in out
    assert "Error: Only X, O, and - are allowed." in out
    assert "No winner yet." in out
    assert "Invalid option." in out


def test_main_next_player_after_load(monkeypatch, capsys):
    answers = ["3", "6", "X - -;- - -;- - -", "2", "2", "2", "5", "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "Turn: player O" in out
    assert "X - -\n- O -\n- - -" in out


def test_main_files(monkeypatch, capsys, tmp_path):
    path = str(tmp_path / "board.txt")
    missing = str(tmp_path / "missing.txt")
    bad_dir = str(tmp_path / "no_dir" / "board.txt")
    answers = ["3", "2", "1", "1", "8", path, "10", "3", "9", path, "5",
               "9", missing, "8", bad_dir, "0"]
    out = run_main(monkeypatch, capsys, answers)
    assert "Board saved." in out
    assert "Board loaded." in out
    assert "X - -\n- - -\n- - -" in out
    assert out.count("Error") == 2
