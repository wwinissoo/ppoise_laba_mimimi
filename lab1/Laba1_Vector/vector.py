"""Three-dimensional vector defined by a start point and an end point."""

import math

def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)

class Vector:
    """
    A vector in three-dimensional space.

    The state is private: the start and end points are tuples of three numbers.
    Supports arithmetic, comparison by length, text conversion and copying.
    """

    def __init__(self, start, end):
        """
        Create a vector from two points.

        :param start: Start point, three numbers.
        :param end: End point, three numbers.
        :raises ValueError: If a point does not have exactly three coordinates.
        :raises TypeError: If a coordinate is not a number.
        """
        if len(start) != 3 or len(end) != 3:
            raise ValueError("Нужно указать 3 координаты.")

        if not all(_is_number(value) for value in (*start, *end)):
            raise TypeError("Координаты должны быть числами.")

        self.__start = tuple(start)
        self.__end = tuple(end)

    def get_start(self):
        """
        Return the coordinates of the start point.
        """
        return self.__start

    def get_end(self):
        """
        Return the coordinates of the end point.
        """
        return self.__end

    def get_x(self):
        """
        Return the X component of the vector.
        """
        return self.__end[0] - self.__start[0]

    def get_y(self):
        """
        Return the Y component of the vector.
        """
        return self.__end[1] - self.__start[1]

    def get_z(self):
        """
        Return the Z component of the vector.
        """
        return self.__end[2] - self.__start[2]

    def length(self):
        """
        Return the Euclidean length of the vector.
        """
        x = self.get_x()
        y = self.get_y()
        z = self.get_z()

        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def __add__(self, other):
        """
        Add two vectors component-wise.
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
        Add in place (``+=``) and return the modified vector.
        """
        result = self + other
        self.__end = result.get_end()

        return self

    def __sub__(self, other):
        """
        Subtract two vectors component-wise.
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
        Subtract in place (``-=``) and return the modified vector.
        """
        result = self - other
        self.__end = result.get_end()

        return self

    def __mul__(self, other):
        """
        Return the cross product (vector operand) or multiply by a number.
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
        Support ``number * vector``.
        """
        return self * number

    def __imul__(self, other):
        """
        Multiply in place (``*=``) and return the modified vector.
        """
        result = self * other
        self.__end = result.get_end()

        return self

    def __truediv__(self, number):
        """
        Divide the vector by a number.
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
        Divide in place (``/=``) and return the modified vector.
        """
        result = self / number
        self.__end = result.get_end()

        return self

    def cosine(self, other):
        """
        Return the cosine of the angle between two vectors.
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
        Check whether two vectors are equal.
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
        Check whether two vectors are not equal.
        """
        return not self == other

    def __hash__(self):
        """
        Return a hash computed from the vector components.

        Equal vectors have equal hashes. The in-place operations
        (``+=``, ``-=``, ``*=``, ``/=``) modify the vector, so do not
        modify a vector while it is stored in a ``set`` or used as a ``dict`` key.
        """
        return hash((self.get_x(), self.get_y(), self.get_z()))

    def __lt__(self, other):
        """
        Check whether this vector is shorter than the other.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() < other.length()

    def __le__(self, other):
        """
        Check whether this vector is not longer than the other.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() <= other.length()

    def __gt__(self, other):
        """
        Check whether this vector is longer than the other.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() > other.length()

    def __ge__(self, other):
        """
        Check whether this vector is not shorter than the other.
        """

        if not isinstance(other, Vector):
            raise TypeError("Нужен второй вектор.")

        return self.length() >= other.length()

    def __str__(self):
        """
        Return a human-readable description of the vector.
        """
        return f"Начало: {self.__start}, конец: {self.__end}"

    def __repr__(self):
        """
        Return a string that can recreate the object.
        """
        return f"Vector({self.__start}, {self.__end})"

    def to_string(self):
        """
        Convert the vector to a string of the form ``"x1 y1 z1 x2 y2 z2"``.
        """
        return (
            f"{self.__start[0]} {self.__start[1]} {self.__start[2]} "
            f"{self.__end[0]} {self.__end[1]} {self.__end[2]}"
        )

    @classmethod
    def from_string(cls, text):
        """
        Create a vector from a string of the form ``"x1 y1 z1 x2 y2 z2"``.

        Raises:
            ValueError: If the text does not contain exactly six numbers or contains a non-number.
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
        Return an independent copy of the vector.
        """
        return Vector(self.__start, self.__end)