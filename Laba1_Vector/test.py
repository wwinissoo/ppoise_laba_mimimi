import math
import copy

import pytest

from vector import Vector


def test_start_and_end():
    vector = Vector((1, 2, 3), (4, 5, 6))

    assert vector.get_start() == (1, 2, 3)
    assert vector.get_end() == (4, 5, 6)


def test_wrong_coordinates():
    with pytest.raises(ValueError):
        Vector((1, 2), (3, 4, 5))


def test_not_number_coordinates():
    with pytest.raises(TypeError):
        Vector("abc", "def")

    with pytest.raises(TypeError):
        Vector((True, 0, 0), (1, 2, 3))


def test_x():
    vector = Vector((1, 2, 3), (6, 8, 10))

    assert vector.get_x() == 5


def test_y():
    vector = Vector((1, 2, 3), (6, 8, 10))

    assert vector.get_y() == 6


def test_z():
    vector = Vector((1, 2, 3), (6, 8, 10))

    assert vector.get_z() == 7


def test_length():
    vector = Vector((0, 0, 0), (3, 4, 0))

    assert vector.length() == 5


def test_add():
    first = Vector((0, 0, 0), (1, 2, 3))
    second = Vector((0, 0, 0), (4, 5, 6))

    result = first + second

    assert result.get_x() == 5
    assert result.get_y() == 7
    assert result.get_z() == 9


def test_add_assign():
    first = Vector((0, 0, 0), (1, 2, 3))
    second = Vector((0, 0, 0), (4, 5, 6))

    first += second

    assert first.get_x() == 5
    assert first.get_y() == 7
    assert first.get_z() == 9


def test_add_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector + 5


def test_subtract():
    first = Vector((0, 0, 0), (8, 7, 6))
    second = Vector((0, 0, 0), (3, 2, 1))

    result = first - second

    assert result.get_x() == 5
    assert result.get_y() == 5
    assert result.get_z() == 5


def test_subtract_assign():
    first = Vector((0, 0, 0), (8, 7, 6))
    second = Vector((0, 0, 0), (3, 2, 1))

    first -= second

    assert first.get_x() == 5
    assert first.get_y() == 5
    assert first.get_z() == 5


def test_subtract_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector - 5


def test_cross_product():
    first = Vector((0, 0, 0), (1, 0, 0))
    second = Vector((0, 0, 0), (0, 1, 0))

    result = first * second

    assert result.get_x() == 0
    assert result.get_y() == 0
    assert result.get_z() == 1


def test_cross_product_assign():
    first = Vector((0, 0, 0), (1, 0, 0))
    second = Vector((0, 0, 0), (0, 1, 0))

    first *= second

    assert first.get_x() == 0
    assert first.get_y() == 0
    assert first.get_z() == 1


def test_multiply():
    vector = Vector((0, 0, 0), (2, 3, 4))

    result = vector * 3

    assert result.get_x() == 6
    assert result.get_y() == 9
    assert result.get_z() == 12


def test_multiply_from_left():
    vector = Vector((0, 0, 0), (2, 3, 4))

    result = 3 * vector

    assert result.get_x() == 6
    assert result.get_y() == 9
    assert result.get_z() == 12


def test_multiply_assign():
    vector = Vector((0, 0, 0), (2, 3, 4))

    vector *= 2

    assert vector.get_x() == 4
    assert vector.get_y() == 6
    assert vector.get_z() == 8


def test_multiply_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector * "abc"


def test_divide():
    vector = Vector((0, 0, 0), (8, 6, 4))

    result = vector / 2

    assert result.get_x() == 4
    assert result.get_y() == 3
    assert result.get_z() == 2


def test_divide_assign():
    vector = Vector((0, 0, 0), (8, 6, 4))

    vector /= 2

    assert vector.get_x() == 4
    assert vector.get_y() == 3
    assert vector.get_z() == 2


def test_divide_by_zero():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(ZeroDivisionError):
        vector / 0


def test_divide_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector / "abc"


def test_cosine_zero():
    first = Vector((0, 0, 0), (1, 0, 0))
    second = Vector((0, 0, 0), (0, 1, 0))

    assert math.isclose(first.cosine(second), 0)


def test_cosine_one():
    first = Vector((0, 0, 0), (2, 0, 0))
    second = Vector((0, 0, 0), (5, 0, 0))

    assert math.isclose(first.cosine(second), 1)


def test_cosine_minus_one():
    first = Vector((0, 0, 0), (2, 0, 0))
    second = Vector((0, 0, 0), (-5, 0, 0))

    assert math.isclose(first.cosine(second), -1)


def test_cosine_zero_vector():
    first = Vector((0, 0, 0), (0, 0, 0))
    second = Vector((0, 0, 0), (1, 0, 0))

    with pytest.raises(ValueError):
        first.cosine(second)


def test_cosine_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector.cosine(5)


def test_equal():
    first = Vector((0, 0, 0), (2, 3, 4))
    second = Vector((5, 6, 7), (7, 9, 11))

    assert first == second


def test_not_equal():
    first = Vector((0, 0, 0), (2, 3, 4))
    second = Vector((0, 0, 0), (2, 3, 5))

    assert first != second


def test_equal_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    assert vector != 5


def test_hash_equal_vectors():
    first = Vector((0, 0, 0), (2, 3, 4))
    second = Vector((5, 6, 7), (7, 9, 11))

    assert hash(first) == hash(second)
    assert len({first, second}) == 1


def test_multiply_by_bool_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector * True

    with pytest.raises(TypeError):
        vector / False


def test_copy_is_independent():
    vector = Vector((0, 0, 0), (1, 2, 3))
    duplicate = vector.copy()

    duplicate += Vector((0, 0, 0), (1, 1, 1))

    assert vector.get_end() == (1, 2, 3)
    assert duplicate.get_end() == (2, 3, 4)


def test_less():
    first = Vector((0, 0, 0), (2, 0, 0))
    second = Vector((0, 0, 0), (5, 0, 0))

    assert first < second


def test_less_equal():
    first = Vector((0, 0, 0), (3, 0, 0))
    second = Vector((0, 0, 0), (3, 0, 0))

    assert first <= second


def test_greater():
    first = Vector((0, 0, 0), (8, 0, 0))
    second = Vector((0, 0, 0), (3, 0, 0))

    assert first > second


def test_greater_equal():
    first = Vector((0, 0, 0), (8, 0, 0))
    second = Vector((0, 0, 0), (8, 0, 0))

    assert first >= second


def test_comparison_wrong():
    vector = Vector((0, 0, 0), (1, 2, 3))

    with pytest.raises(TypeError):
        vector > 5

    with pytest.raises(TypeError):
        vector >= 5

    with pytest.raises(TypeError):
        vector < 5

    with pytest.raises(TypeError):
        vector <= 5


def test_str():
    vector = Vector((1, 2, 3), (4, 5, 6))

    result = str(vector)

    assert "Начало" in result
    assert "конец" in result


def test_repr():
    vector = Vector((1, 2, 3), (4, 5, 6))

    assert repr(vector) == "Vector((1, 2, 3), (4, 5, 6))"


def test_to_string():
    vector = Vector((1, 2, 3), (4, 5, 6))

    assert vector.to_string() == "1 2 3 4 5 6"


def test_from_string():
    vector = Vector.from_string("1 2 3 4 5 6")

    assert vector.get_start() == (1.0, 2.0, 3.0)
    assert vector.get_end() == (4.0, 5.0, 6.0)


def test_string_round_trip():
    vector = Vector((1.5, -2, 3), (4, 5, 6.25))

    assert Vector.from_string(vector.to_string()) == vector


def test_from_string_wrong_amount():
    with pytest.raises(ValueError):
        Vector.from_string("1 2 3")


def test_from_string_wrong_data():
    with pytest.raises(ValueError):
        Vector.from_string("1 2 hello 4 5 6")


def test_copy():
    vector = Vector((1, 2, 3), (4, 5, 6))

    duplicate = vector.copy()

    assert duplicate == vector
    assert duplicate is not vector


def test_copy_module():
    vector = Vector((1, 2, 3), (4, 5, 6))

    duplicate = copy.copy(vector)

    assert duplicate is not vector
    assert duplicate == vector