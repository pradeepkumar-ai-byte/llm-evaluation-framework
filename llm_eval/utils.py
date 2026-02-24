import math
import random
from typing import Iterable, List


def set_global_seed(seed: int) -> None:
    """
    Set deterministic global seed.
    """
    random.seed(seed)


def mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("Cannot compute mean of empty list.")
    return sum(values) / len(values)


def variance(values: Iterable[float]) -> float:
    values = list(values)
    if len(values) < 2:
        raise ValueError("Variance requires at least two values.")
    m = mean(values)
    return sum((x - m) ** 2 for x in values) / (len(values) - 1)


def standard_deviation(values: Iterable[float]) -> float:
    return math.sqrt(variance(values))


def confidence_interval(
    values: List[float], confidence_level: float
) -> float:
    """
    Returns margin of error for given confidence level
    using normal approximation (large-sample assumption).
    """
    if not values:
        raise ValueError("Cannot compute confidence interval on empty list.")

    z = 1.96  # 95% default normal approximation
    if confidence_level != 0.95:
        raise ValueError("Currently only 95% confidence supported.")

    sd = standard_deviation(values)
    n = len(values)
    return z * (sd / math.sqrt(n))
