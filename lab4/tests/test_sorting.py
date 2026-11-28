from array import array

import pytest

from generic_lab import bubble_sort, patience_sort
from generic_lab.models import Student

ALGORITHMS = [bubble_sort, patience_sort]


@pytest.mark.parametrize("sort", ALGORITHMS)
@pytest.mark.parametrize("data", [[], [1], [3, 1, 2], [2, 2, 1, 1], [1, 2, 3], [3, 2, 1], [-5, 10, 0, 7]])
def test_matches_builtin_sorted(sort, data):
    items = list(data)
    sort(items)
    assert items == sorted(data)


@pytest.mark.parametrize("sort", ALGORITHMS)
def test_reverse(sort):
    items = [3, 1, 2]
    sort(items, reverse=True)
    assert items == [3, 2, 1]


@pytest.mark.parametrize("sort", ALGORITHMS)
def test_sorts_array_and_strings(sort):
    numbers = array("i", [4, 3, 9, 1])
    sort(numbers)
    words = ["pear", "apple", "fig"]
    sort(words, key=len)
    assert list(numbers) == [1, 3, 4, 9]
    assert words == ["fig", "pear", "apple"]


@pytest.mark.parametrize("sort", ALGORITHMS)
def test_sorts_custom_objects_and_is_stable(sort):
    students = [Student(9.0, "B"), Student(7.0, "A"), Student(9.0, "A")]
    sort(students)
    assert [s.name for s in students] == ["A", "A", "B"]
    pairs = [(1, "x"), (0, "y"), (1, "z"), (0, "w")]
    sort(pairs, key=lambda pair: pair[0])
    assert pairs == [(0, "y"), (0, "w"), (1, "x"), (1, "z")]
