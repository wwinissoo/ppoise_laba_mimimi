from vector import Vector


def input_point(title):
    print(title)

    x = float(input("  X: "))
    y = float(input("  Y: "))
    z = float(input("  Z: "))

    return x, y, z


def input_vector():
    start = input_point("Начальная точка")
    end = input_point("Конечная точка")

    return Vector(start, end)


def print_vector(name, vector):
    print(name)
    print(f"  Начало: {vector.get_start()}")
    print(f"  Конец: {vector.get_end()}")

    print(
        f"  Компоненты: "
        f"({vector.get_x()}, "
        f"{vector.get_y()}, "
        f"{vector.get_z()})"
    )

    print(f"  Длина: {vector.length()}")


def print_menu():
    print()
    print("========== ВЕКТОРЫ ==========")
    print("1 - Создать векторы")
    print("2 - Показать векторы")
    print("3 - Сложить")
    print("4 - Вычесть")
    print("5 - Векторное произведение")
    print("6 - Умножить первый вектор на число")
    print("7 - Разделить первый вектор на число")
    print("8 - Косинус угла")
    print("9 - Сравнить длины")
    print("10 - Проверить равенство")
    print("11 - Сохранить в строку")
    print("12 - Загрузить из строки")
    print("13 - Скопировать первый вектор")
    print("0 - Выход")
    print("==============================")


def main():

    first = None
    second = None

    while True:

        print_menu()

        command = input("Выберите действие: ")

        if command == "0":
            print("Работа завершена.")
            return

        elif command == "1":

            try:
                print("\nПервый вектор:")
                new_first = input_vector()

                print("\nВторой вектор:")
                new_second = input_vector()

                first, second = new_first, new_second

                print("\nВекторы успешно созданы.")

            except (ValueError, TypeError) as error:
                print(f"Ошибка: {error}")

        elif command == "2":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            print()
            print_vector("Первый вектор:", first)

            print()
            print_vector("Второй вектор:", second)

        elif command == "3":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            result = first + second

            print_vector("Результат сложения:", result)

        elif command == "4":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            result = first - second

            print_vector("Результат вычитания:", result)

        elif command == "5":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            result = first * second

            print_vector("Векторное произведение:", result)

        elif command == "6":

            if first is None:
                print("Сначала создайте первый вектор.")
                continue

            try:
                number = float(input("Введите число: "))

                result = first * number

                print_vector("Результат:", result)

            except (ValueError, TypeError) as error:
                print(f"Ошибка: {error}")

        elif command == "7":

            if first is None:
                print("Сначала создайте первый вектор.")
                continue

            try:
                number = float(input("Введите число: "))

                result = first / number

                print_vector("Результат:", result)

            except (ValueError, ZeroDivisionError, TypeError) as error:
                print(f"Ошибка: {error}")

        elif command == "8":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            try:
                value = first.cosine(second)

                print(f"Косинус угла = {value}")

            except (ValueError, TypeError) as error:
                print(f"Ошибка: {error}")

        elif command == "9":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            if first > second:
                print("Первый вектор длиннее.")

            elif first < second:
                print("Второй вектор длиннее.")

            else:
                print("Длины векторов одинаковы.")

        elif command == "10":

            if first is None or second is None:
                print("Сначала создайте оба вектора.")
                continue

            if first == second:
                print("Векторы равны.")

            else:
                print("Векторы различаются.")

        elif command == "11":

            if first is None:
                print("Сначала создайте первый вектор.")
                continue

            text = first.to_string()

            print("Строка:")
            print(text)

        elif command == "12":

            text = input(
                "Введите координаты "
                "(x1 y1 z1 x2 y2 z2): "
            )

            try:
                first = Vector.from_string(text)

                print("Вектор успешно загружен.")

                print_vector(
                    "Загруженный вектор:",
                    first
                )

            except (ValueError, TypeError) as error:
                print(f"Ошибка: {error}")

        elif command == "13":

            if first is None:
                print("Сначала создайте первый вектор.")
                continue

            result = first.copy()

            print_vector("Копия первого вектора:", result)

        else:
            print("Такого пункта нет.")


if __name__ == "__main__":
    main()