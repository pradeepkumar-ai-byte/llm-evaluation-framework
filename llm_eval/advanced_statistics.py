"""
Advanced Statistical Methods

Author: Pradeep Kumar

Implements bootstrap-based significance testing.
"""

import random
from typing import Dict, List

from .models import Dataset
from .config import Config
from .utils import mean, set_global_seed
from .exceptions import StatisticalComputationError


def bootstrap_significance_test(
    dataset: Dataset,
    config: Config,
) -> Dict[str, float]:
    """
    Perform bootstrap significance testing between two groups.

    Returns:
        {
            "observed_mean_difference": float,
            "empirical_p_value": float,
            "significant": bool
        }
    """

    try:
        set_global_seed(config.random_seed)

        group_scores = _collect_group_scores(dataset)

        if len(group_scores) != 2:
            raise StatisticalComputationError(
                "Bootstrap requires exactly two groups."
            )

        groups = list(group_scores.keys())
        group_a = group_scores[groups[0]]
        group_b = group_scores[groups[1]]

        observed_diff = mean(group_a) - mean(group_b)

        combined = group_a + group_b
        n_a = len(group_a)

        count_extreme = 0

        for _ in range(config.bootstrap_iterations):
            resample = random.choices(combined, k=len(combined))

            resample_a = resample[:n_a]
            resample_b = resample[n_a:]

            diff = mean(resample_a) - mean(resample_b)

            if abs(diff) >= abs(observed_diff):
                count_extreme += 1

        empirical_p = count_extreme / config.bootstrap_iterations

        return {
            "observed_mean_difference": observed_diff,
            "empirical_p_value": empirical_p,
            "significant": empirical_p < config.significance_alpha,
        }

    except Exception as e:
        raise StatisticalComputationError(
            f"Bootstrap significance failed: {str(e)}"
        )


def _collect_group_scores(dataset: Dataset) -> Dict[str, List[float]]:
    group_scores: Dict[str, List[float]] = {}

    for entry in dataset:
        entry_mean = mean(entry.scores.values())
        group = entry.metadata.group

        if group not in group_scores:
            group_scores[group] = []

        group_scores[group].append(entry_mean)

    return group_scores
