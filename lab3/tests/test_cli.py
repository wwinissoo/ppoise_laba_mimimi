from datetime import date

import pytest

import main
from cli.console import FitnessConsole, create_library
from tests.conftest import NOW

REGISTER = ["1", "anna", "anna@mail.ru", "Secret123", "2000-05-20", "ж"]
LOGIN = ["2", "anna", "Secret123"]
WORKOUT = ["4", "Ноги", "Приседания", "10", "60", "8", "д", "Жим лёжа", "5", "80,5", "9", "н"]
MEAL = ["5", "обед", "Курица", "165", "31", "3.6", "0", "200"]


def run_console(answers):
    output = []
    feed = iter(answers)
    console = FitnessConsole(read=lambda prompt: next(feed), write=output.append, clock=lambda: NOW)
    console.run()
    return console, "\n".join(output)


class TestFitnessConsole:
    def test_full_session(self):
        answers = ["4", *REGISTER, *LOGIN, "3", "60", "170", *WORKOUT, *MEAL, "6", "7", "8", "8", "x", "9", "0"]
        console, text = run_console(answers)
        assert "Ошибка: Сначала войдите в аккаунт" in text and "Пользователь anna зарегистрирован" in text
        assert "Добро пожаловать, anna!" in text and "ИМТ 20.8 — норма" in text
        assert "Тренировка сохранена: 2 подходов, объём 1002.5 кг" in text
        assert "Получено достижение: Первая тренировка" in text
        assert "Съедено 330.0 ккал, осталось 1797.0 ккал" in text and "anna: 1 тренировок" in text
        assert "- Жим лёжа [силовое], сложность 3/5" in text and "[ ] Тренировка завершена" in text
        assert "[x] Новое достижение: Первая тренировка" in text
        assert "Неизвестный пункт меню" in text and "Вы вышли из аккаунта" in text and text.endswith("До встречи!")
        assert console.tracker.current_user is None

    @pytest.mark.parametrize(
        "answers, message",
        [
            (["1", "anna", "a@a.ru", "Secret123", "20.05.2000"], "формате ГГГГ-ММ-ДД"),
            ([*REGISTER, *LOGIN, "3", "много"], "Нужно ввести число"),
            ([*REGISTER, *LOGIN, "4", "Ноги", "Приседания", "2.5"], "целое число"),
            ([*REGISTER, *LOGIN, "4", "Ноги", "Бокс", "10", "60", "8"], "не найден"),
        ],
    )
    def test_input_errors(self, answers, message):
        _, text = run_console([*answers, "0"])
        assert message in text

    def test_empty_notifications_and_guest_menu(self):
        _, text = run_console([*REGISTER, *LOGIN, "8", "0"])
        assert "Уведомлений нет" in text and "=== Фитнес-трекер (гость) ===" in text

    def test_defaults(self):
        console = FitnessConsole()
        assert len(console.tracker.library.exercises) == len(create_library().exercises) == 22


class TestMain:
    def test_main_runs_console(self, monkeypatch):
        calls = []
        monkeypatch.setattr(main.FitnessConsole, "run", lambda self: calls.append(self))
        main.main()
        assert len(calls) == 1

    @pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
    def test_main_handles_interrupt(self, monkeypatch, capsys, error):
        def interrupt(self):
            raise error

        monkeypatch.setattr(main.FitnessConsole, "run", interrupt)
        main.main()
        assert "Работа завершена" in capsys.readouterr().out
        assert date.today()
