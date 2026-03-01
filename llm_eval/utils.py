import math
import random
from typing import Iterable


def set_global_seed(seed: int) -> None:
    """
    Set deterministic global seed.
    """
    random.seed(seed)


def mean(values: Iterable[float]) -> float:
    values_list = list(values)
    if not values_list:
        raise ValueError("Cannot compute mean of empty list.")
    return sum(values_list) / len(values_list)


def variance(values: Iterable[float]) -> float:
    values_list = list(values)
    if len(values_list) < 2:
        raise ValueError("Variance requires at least two values.")
    m = mean(values_list)
    return sum((x - m) ** 2 for x in values_list) / (len(values_list) - 1)


def standard_deviation(values: Iterable[float]) -> float:
    return math.sqrt(variance(values))


def confidence_interval(
    values: Iterable[float],
    confidence_level: float,
) -> float:
    """
    Returns margin of error for given confidence level
    using normal approximation (large-sample assumption).
    """
    values_list = list(values)

    if not values_list:
        raise ValueError(
            "Cannot compute confidence interval on empty list."
        )

    z = 1.96  # 95% default normal approximation

    if confidence_level != 0.95:
        raise ValueError(
            "Currently only 95% confidence supported."
        )

    sd = standard_deviation(values_list)
    n = len(values_list)

    return z * (sd / math.sqrt(n))