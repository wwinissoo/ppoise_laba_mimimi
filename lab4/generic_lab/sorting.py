"""Generic in-place sorting for any mutable sequence (list, array.array, ...)."""

from bisect import bisect_left
from heapq import merge
from typing import Any, Callable, MutableSequence, Optional, TypeVar

T = TypeVar("T")
KeyFunction = Optional[Callable[[T], Any]]


def _identity(value: T) -> T:
    return value


def _is_out_of_order(left_key: Any, right_key: Any, reverse: bool) -> bool:
    return left_key < right_key if reverse else right_key < left_key


def _bubble_pass(items: MutableSequence[T], end: int, key: Callable[[T], Any], reverse: bool) -> bool:
    """Move the extreme element of items[:end + 1] to the end. Return True if anything was swapped."""
    swapped = False
    for index in range(end):
        if _is_out_of_order(key(items[index]), key(items[index + 1]), reverse):
            items[index], items[index + 1] = items[index + 1], items[index]
            swapped = True
    return swapped


def bubble_sort(items: MutableSequence[T], key: KeyFunction = None, reverse: bool = False) -> None:
    """Sort items in place with bubble sort (stable, stops early on a sorted input)."""
    key_function = key or _identity
    for end in range(len(items) - 1, 0, -1):
        if not _bubble_pass(items, end, key_function, reverse):
            break


def _deal_into_piles(items: MutableSequence[T], key: Callable[[T], Any]) -> list:
    """Deal items onto piles: each card goes onto the leftmost pile whose top is not smaller."""
    piles: list = []
    tops: list = []
    for index, item in enumerate(items):
        card = (key(item), index)
        pile_number = bisect_left(tops, card)
        if pile_number == len(piles):
            piles.append([])
            tops.append(card)
        tops[pile_number] = card
        piles[pile_number].append((card, item))
    return piles


def patience_sort(items: MutableSequence[T], key: KeyFunction = None, reverse: bool = False) -> None:
    """Sort items in place with patience sorting (deal into piles, then merge the piles).

    The ascending order is stable; with reverse=True the ascending result is simply reversed.
    """
    piles = _deal_into_piles(items, key or _identity)
    merged = merge(*(reversed(pile) for pile in piles), key=lambda pair: pair[0])
    ordered = [item for _, item in merged]
    if reverse:
        ordered.reverse()
    for index, item in enumerate(ordered):
        items[index] = item
