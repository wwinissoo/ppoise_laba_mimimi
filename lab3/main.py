"""Точка входа консольного приложения фитнес-трекера."""

from cli.console import FitnessConsole


def main():
    try:
        FitnessConsole().run()
    except (EOFError, KeyboardInterrupt):
        print("\nРабота завершена.")


if __name__ == "__main__":
    main()
