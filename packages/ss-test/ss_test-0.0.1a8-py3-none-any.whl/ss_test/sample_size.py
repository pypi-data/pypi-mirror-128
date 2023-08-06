from typing import List

from numpy import mean
from statsmodels.stats.power import TTestIndPower


def get_mean(numbers: List[int]) -> int:
    return mean(numbers)  # type: ignore


def get_sample_size(effect_size: float) -> int:
    obj = TTestIndPower()
    n = obj.solve_power(effect_size=effect_size, alpha=0.05, power=0.8, ratio=1, alternative="two-sided")
    if not isinstance(n, float):
        return 0
    return round(n, 0)  # type: ignore
