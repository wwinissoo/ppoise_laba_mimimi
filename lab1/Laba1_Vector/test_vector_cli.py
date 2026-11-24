import importlib.util
from pathlib import Path

import pytest

MAIN_PATH = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("vector_cli", MAIN_PATH)
vector_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vector_cli)

ORIGIN = ["0", "0", "0"]


def point(x, y, z):
    return [str(x), str(y), str(z)]


def create(first_end, second_end):
    return ["1", *ORIGIN, *point(*first_end), *ORIGIN, *point(*second_end)]


def run(monkeypatch, capsys, *answers):
    script = iter([*answers, "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(script))
    vector_cli.main()
    return capsys.readouterr().out


def test_exit(monkeypatch, capsys):
    assert "Работа завершена." in run(monkeypatch, capsys)


@pytest.mark.parametrize("command", ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "13"])
def test_commands_need_vectors(monkeypatch, capsys, command):
    assert "Сначала создайте" in run(monkeypatch, capsys, command)


def test_unknown_command(monkeypatch, capsys):
    assert "Такого пункта нет." in run(monkeypatch, capsys, "99")


def test_full_session(monkeypatch, capsys):
    out = run(
        monkeypatch, capsys, *create((3, 4, 0), (0, 0, 4)), "2", "3", "4", "5", "6", "2", "7", "2", "8", "9", "10", "11", "13"
    )
    for text in ["Векторы успешно созданы.", "Первый вектор:", "Результат сложения:", "Результат вычитания:"]:
        assert text in out
    for text in ["Векторное произведение:", "Косинус угла = 0.0", "Первый вектор длиннее.", "Векторы различаются."]:
        assert text in out
    assert "0.0 0.0 0.0 3.0 4.0 0.0" in out and "Копия первого вектора:" in out


def test_compare_lengths_and_equality(monkeypatch, capsys):
    shorter = run(monkeypatch, capsys, *create((1, 0, 0), (0, 2, 0)), "9")
    equal = run(monkeypatch, capsys, *create((1, 0, 0), (1, 0, 0)), "9", "10")
    assert "Второй вектор длиннее." in shorter
    assert "Длины векторов одинаковы." in equal and "Векторы равны." in equal


def test_load_from_string(monkeypatch, capsys):
    out = run(monkeypatch, capsys, "12", "0 0 0 1 1 1")
    assert "Вектор успешно загружен." in out and "Загруженный вектор:" in out


def test_input_errors(monkeypatch, capsys):
    out = run(monkeypatch, capsys, "1", "abc")
    out += run(monkeypatch, capsys, *create((1, 0, 0), (0, 0, 0)), "6", "x", "7", "0", "7", "x", "8")
    out += run(monkeypatch, capsys, "12", "1 2 3")
    assert out.count("Ошибка:") == 6
