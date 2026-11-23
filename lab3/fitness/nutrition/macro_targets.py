from fitness.exceptions import InvalidValueError
from fitness.nutrition.constants import CARB_KCAL, FAT_KCAL, PROTEIN_KCAL
from fitness.validation import ensure_number, ensure_positive


class MacroTargets:
    """Суточная норма белков, жиров и углеводов в граммах."""

    def __init__(self, protein_g, fat_g, carbs_g):
        self._protein_g = ensure_number(protein_g, "белки", minimum=0)
        self._fat_g = ensure_number(fat_g, "жиры", minimum=0)
        self._carbs_g = ensure_number(carbs_g, "углеводы", minimum=0)

    @classmethod
    def from_calories(cls, calories, protein_share=0.3, fat_share=0.25):
        ensure_positive(calories, "калории")
        if protein_share + fat_share >= 1:
            raise InvalidValueError("Доли белков и жиров должны оставлять место углеводам")
        carbs_share = 1 - protein_share - fat_share
        return cls(
            round(calories * protein_share / PROTEIN_KCAL),
            round(calories * fat_share / FAT_KCAL),
            round(calories * carbs_share / CARB_KCAL),
        )

    @property
    def protein_g(self):
        return self._protein_g

    @property
    def fat_g(self):
        return self._fat_g

    @property
    def carbs_g(self):
        return self._carbs_g

    def as_dict(self):
        return {"белки": self._protein_g, "жиры": self._fat_g, "углеводы": self._carbs_g}

    def calories(self):
        return self._protein_g * PROTEIN_KCAL + self._fat_g * FAT_KCAL + self._carbs_g * CARB_KCAL

    def deviation(self, actual):
        """Отклонение факта от нормы по каждому макронутриенту, г."""
        return {macro: round(actual.get(macro, 0) - target, 1) for macro, target in self.as_dict().items()}

    def is_balanced(self, actual, tolerance_percent=10):
        for macro, target in self.as_dict().items():
            allowed = target * tolerance_percent / 100
            if abs(actual.get(macro, 0) - target) > allowed:
                return False
        return True
