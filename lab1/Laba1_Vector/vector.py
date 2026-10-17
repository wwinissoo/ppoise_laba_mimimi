import math

def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)



class Vector:
    
    def __init__(self, start, end):
        if len(start) != 3 or len(end) != 3:
            raise ValueError("Нужно указать 3 координаты.")

        if not all(_is_number(value) for value in (*start, *end)):
            raise TypeError("Координаты должны быть числами.")

        self.__start = tuple(start)
        self.__end = tuple(end)

    def get_start(self):
        """
        Возвращает координаты начала вектора.
        """
        return self.__start

    def get_end(self):
        """
        Возвращает координаты конца вектора.
        """
        return self.__end

    def get_x(self):
        """
        Возвращает координату X вектора.
        """
        return self.__end[0] - self.__start[0]

    def get_y(self):
        """
        Возвращает координату Y вектора.
        """
        return self.__end[1] - self.__start[1]

    def get_z(self):
        """
        Возвращает координату Z вектора.
        """
        return self.__end[2] - self.__start[2]

    def length(self):
        """
        Вычисляет длину вектора.
        """
        x = self.get_x()
        y = self.get_y()
        z = self.get_z()

        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def __add__(self, other):
        """
        Сложение двух векторов.
        """
        if not isinstance(other, Vector):
            raise TypeError("Можно складывать только векторы.")

        x = self.get_x() + other.get_x()
        y = self.get_y() + other.get_y()
        z = self.get_z() + other.get_z()

        sum = (
            self.__start[0] + x,
            self.__start[1] + y,
            self.__start[2] + z
        )

        return Vector(self.__start, sum)

    def __iadd__(self, other):
        """
        Сложение с присваиванием.
        """
        result = self + other
        self.__end = result.get_end()

        return self

    def __sub__(self, other):
        """
        Вычитание двух векторов.
        """
        if not isinstance(other, Vector):
            raise TypeError("Можно вычитать только векторы.")

        x = self.get_x() - other.get_x()
        y = self.get_y() - other.get_y()
        z = self.get_z() - other.get_z()

        difference = (
            self.__start[0] + x,
            self.__start[1] + y,
            self.__start[2] + z
        )

        return Vector(self.__start, difference)

    def __isub__(self, other):
        """
        Вычитание с присваиванием.
        """
        result = self - other
        self.__end = result.get_end()

        return self

    def __mul__(self, other):
        """
        Векторное произведение или умножение на число.
        """

        if isinstance(other, Vector):

            x1 = self.get_x()
            y1 = self.get_y()
            z1 = self.get_z()

            x2 = other.get_x()
            y2 = other.get_y()
            z2 = other.get_z()

            x = y1 * z2 - z1 * y2
            y = z1 * x2 - x1 * z2
            z = x1 * y2 - y1 * x2

            multiply = (
                self.__start[0] + x,
                self.__start[1] + y,
                self.__start[2] + z
            )

            return Vector(self.__start, multiply)

        if _is_number(other):

            x = self.get_x() * other
            y = self.get_y() * other
            z = self.get_z() * other

            multiply = (
                self.__start[0] + x,
                self.__start[1] + y,
                self.__start[2] + z
            )

            return Vector(self.__start, multiply)

        raise TypeError("Умножать можно на вектор или число.")

    def __rmul__(self, number):
        """
        Умножение числа на вектор.
        """
        return self * number

    def __imul__(self, other):
        """
        Умножение с присваиванием.
        """
        result = self * other
        self.__end = result.get_end()

        return self

    def __truediv__(self, number):
        """
        Деление вектора на число.
        """

        if not _is_number(number):
            raise TypeError("Делить можно только на число.")

        if number == 0:
            raise ZeroDivisionError("На ноль делить нельзя.")

        x = self.get_x() / number
        y = self.get_y() / number
        z = self.get_z() / number

        divide = (
            self.__start[0] + x,
            self.__start[1] + y,
            self.__start[2] + z
        )

        return Vector(self.__start, divide)

    def __itruediv__(self, number):
        """
        Деление с присваиванием.
        """
        result = self / number
        self.__end = result.get_end()

        return self

    def cosine(self, other):
        """
        Вычисляет косинус угла между двумя векторами.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        length1 = self.length()
        length2 = other.length()

        if length1 == 0 or length2 == 0:
            raise ValueError("Нельзя определить угол нулевого вектора.")

        x = self.get_x() * other.get_x()
        y = self.get_y() * other.get_y()
        z = self.get_z() * other.get_z()

        scalar = x + y + z

        return scalar / (length1 * length2)

    def __eq__(self, other):
        """
        Проверяет равенство двух векторов.
        """
        if not isinstance(other, Vector):
            return False

        return (
            self.get_x() == other.get_x()
            and self.get_y() == other.get_y()
            and self.get_z() == other.get_z()
        )

    def __ne__(self, other):
        """
        Проверяет неравенство двух векторов.
        """
        return not self == other

    def __hash__(self):
        """
        Возвращает хеш вектора по его компонентам.

        Равные векторы имеют одинаковый хеш. Составные операции
        (``+=``, ``-=``, ``*=``, ``/=``) изменяют вектор, поэтому
        не следует изменять вектор, пока он хранится в ``set`` или ``dict``.
        """
        return hash((self.get_x(), self.get_y(), self.get_z()))

    def __lt__(self, other):
        """
        Проверяет, короче ли первый вектор второго.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() < other.length()

    def __le__(self, other):
        """
        Проверяет, не длиннее ли первый вектор второго.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() <= other.length()

    def __gt__(self, other):
        """
        Проверяет, длиннее ли первый вектор второго.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() > other.length()

    def __ge__(self, other):
        """
        Проверяет, не короче ли первый вектор второго.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() >= other.length()

    def __str__(self):
        """
        Выводит информацию о векторе.
        """
        return f"Начало: {self.__start}, конец: {self.__end}"

    def __repr__(self):
        """
        Возвращает представление объекта.
        """
        return f"Vector({self.__start}, {self.__end})"

    def to_string(self):
        """
        Преобразует вектор в строку формата ``"x1 y1 z1 x2 y2 z2"``.
        """
        return (
            f"{self.__start[0]} {self.__start[1]} {self.__start[2]} "
            f"{self.__end[0]} {self.__end[1]} {self.__end[2]}"
        )

    @classmethod
    def from_string(cls, text):
        """
        Создает вектор из строки формата ``"x1 y1 z1 x2 y2 z2"``.

        Raises:
            ValueError: если чисел не 6 или строка содержит не числа.
        """

        values = text.split()

        if len(values) != 6:
            raise ValueError("Нужно указать 6 координат.")

        values = [float(value) for value in values]

        start = (
            values[0],
            values[1],
            values[2]
        )

        end = (
            values[3],
            values[4],
            values[5]
        )

        return cls(start, end)

    def copy(self):
        """
        Создает копию вектора.
        """
        return Vector(self.__start, self.__end)