from generic_lab.cli import Console, run


def run_script(*answers):
    script = iter(answers)
    output = []
    run(Console(lambda prompt: next(script), output.append))
    return "\n".join(output)


def test_exit_and_unknown_choice():
    assert "Неизвестный пункт меню" in run_script("x", "0")


def test_sorting_demo():
    text = run_script(
        "1",
        "1",
        "1",
        "n",
        "1",
        "2",
        "д",
        "2",
        "1",
        "1",
        "n",
        "3",
        "2",
        "n",
        "4",
        "1",
        "n",
        "5",
        "3 1 2",
        "2",
        "n",
        "9",
        "1",
        "7",
        "0",
        "0",
    )
    assert "-3, 1, 2, 5, 5, 6, 9  <- Сортировка пузырьком" in text
    assert "9, 6, 5, 5, 2, 1, -3  <- Пасьянсная сортировка" in text
    assert "Анна (9.1)" in text
    assert "1, 2, 3  <- Пасьянсная сортировка" in text
    assert "Неизвестный пункт меню" in text and "Неизвестный алгоритм" in text


def test_sorting_invalid_own_input():
    assert "Ошибка:" in run_script("1", "5", "a b", "0", "0")


def test_graph_demo():
    text = run_script(
        "2",
        "1",
        "A",
        "1",
        "B",
        "1",
        "C",
        "2",
        "1",
        "2",
        "2",
        "2",
        "3",
        "5",
        "6",
        "2",
        "7",
        "1",
        "2",
        "8",
        "9",
        "4",
        "1",
        "2",
        "3",
        "1",
        "5",
        "0",
        "0",
    )
    assert "     1  2  3\n  1  0  1  0\n  2  1  0  1\n  3  0  1  0" in text
    assert "Вершин: 3, рёбер: 2" in text and "  1 (A): 2 (B)\n  2 (B): 1 (A), 3 (C)\n  3 (C): 2 (B)" in text
    assert "Степень: 2" in text and "Степень ребра: 1" in text
    assert "Вершины в обратном порядке: ['C', 'B', 'A']" in text
    assert "копия == оригинал: True" in text and "копия > оригинал=True" in text
    assert "Вершин: 2, рёбер: 1" in text and "  1 (B): 2 (C)" in text


def test_graph_errors():
    text = run_script("2", "1", "A", "2", "1", "1", "3", "9", "3", "x", "7", "1", "1", "42", "0", "0")
    assert text.count("Ошибка:") >= 3


def test_empty_graph_is_readable():
    assert "Граф пуст" in run_script("2", "5", "0", "0")


def test_draw_graph_menu():
    text = run_script("2", "10", "1", "A", "1", "B", "2", "1", "2", "10", "0", "0")
    assert "(добавьте вершины" in text and "(1)" in text and "(2)" in text and "Вершины: (1)=A, (2)=B" in text
