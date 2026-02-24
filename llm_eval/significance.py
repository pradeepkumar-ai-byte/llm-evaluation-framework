"""
Statistical Significance Layer

Author: Pradeep Kumar

Implements:
- Independent two-sample t-test
- Cohen's d effect size
"""

import math
from typing import Dict, List, Tuple

from .config import Config
from .models import Dataset
from .utils import mean, variance
from .exceptions import StatisticalComputationError


def independent_t_test(
    dataset: Dataset,
    config: Config,
) -> Dict[str, float]:
    """
    Perform independent two-sample t-test between groups.
    Assumes exactly two groups.
    """

    try:
        group_scores = _collect_group_scores(dataset)

        if len(group_scores) != 2:
            raise StatisticalComputationError(
                "T-test requires exactly two groups."
            )

        groups = list(group_scores.keys())
        group_a = group_scores[groups[0]]
        group_b = group_scores[groups[1]]

        t_stat = _compute_t_statistic(group_a, group_b)
        p_value = _approximate_two_tailed_p_value(t_stat)

        effect_size = cohen_d(group_a, group_b)

        return {
            "t_statistic": t_stat,
            "p_value": p_value,
            "effect_size_cohen_d": effect_size,
            "significant": p_value < config.significance_alpha,
        }

    except Exception as e:
        raise StatisticalComputationError(
            f"T-test computation failed: {str(e)}"
        )


def cohen_d(group_a: List[float], group_b: List[float]) -> float:
    """
    Compute Cohen's d effect size.
    """

    mean_a = mean(group_a)
    mean_b = mean(group_b)

    var_a = variance(group_a)
    var_b = variance(group_b)

    pooled_sd = math.sqrt(
        ((len(group_a) - 1) * var_a + (len(group_b) - 1) * var_b)
        / (len(group_a) + len(group_b) - 2)
    )

    if pooled_sd == 0:
        return 0.0

    return (mean_a - mean_b) / pooled_sd


def _compute_t_statistic(
    group_a: List[float],
    group_b: List[float],
) -> float:
    mean_a = mean(group_a)
    mean_b = mean(group_b)

    var_a = variance(group_a)
    var_b = variance(group_b)

    n_a = len(group_a)
    n_b = len(group_b)

    pooled_var = (
        ((n_a - 1) * var_a + (n_b - 1) * var_b)
        / (n_a + n_b - 2)
    )

    standard_error = math.sqrt(pooled_var * (1 / n_a + 1 / n_b))

    if standard_error == 0:
        raise StatisticalComputationError(
            "Standard error is zero; cannot compute t-statistic."
        )

    return (mean_a - mean_b) / standard_error


def _approximate_two_tailed_p_value(t_stat: float) -> float:
    """
    Normal approximation for two-tailed p-value.
    Suitable for moderate-to-large sample sizes.
    """

    z = abs(t_stat)
    p_one_tail = 0.5 * (1 - math.erf(z / math.sqrt(2)))
    return 2 * p_one_tail


def _collect_group_scores(dataset: Dataset) -> Dict[str, List[float]]:
    """
    Collect overall mean score per entry grouped by metadata.group.
    """

    group_scores: Dict[str, List[float]] = {}

    for entry in dataset:
        entry_mean = mean(entry.scores.values())
        group = entry.metadata.group

        if group not in group_scores:
            group_scores[group] = []

        group_scores[group].append(entry_mean)

    return group_scores
