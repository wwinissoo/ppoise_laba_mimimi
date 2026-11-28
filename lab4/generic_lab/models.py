"""Sample user-defined class used to demonstrate sorting of custom objects."""

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Student:
    """A student ordered by average grade, then by name."""

    average_grade: float
    name: str

    def __str__(self) -> str:
        return f"{self.name} ({self.average_grade})"
