"""Точка входа консольного приложения кулинарной системы."""

from cli.console import CulinaryConsole


def main():
    try:
        CulinaryConsole().run()
    except (EOFError, KeyboardInterrupt):
        print("\nРабота завершена.")


if __name__ == "__main__":
    main()
