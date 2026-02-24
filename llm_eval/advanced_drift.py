"""
Advanced Drift Detection

Author: Pradeep Kumar

Implements KL-divergence based distribution drift detection.
"""

import math
from typing import Dict, List

from .models import Dataset
from .config import Config
from .exceptions import DriftDetectionError


def detect_kl_drift(
    dataset: Dataset,
    baseline_dataset: Dataset,
    config: Config,
) -> Dict[str, object]:
    """
    Compute KL divergence per dimension and detect drift.

    Returns:
        {
            "dimension_kl": {...},
            "overall_kl": float,
            "drift_detected": bool
        }
    """

    try:
        dimension_kl: Dict[str, float] = {}

        for dim in config.required_dimensions:
            current_dist = _compute_distribution(dataset, dim, config)
            baseline_dist = _compute_distribution(
                baseline_dataset,
                dim,
                config,
            )

            kl_value = _kl_divergence(current_dist, baseline_dist)
            dimension_kl[dim] = kl_value

        overall_kl = sum(dimension_kl.values()) / len(dimension_kl)

        return {
            "dimension_kl": dimension_kl,
            "overall_kl": overall_kl,
            "drift_detected": overall_kl > config.drift_threshold,
        }

    except Exception as e:
        raise DriftDetectionError(
            f"KL drift detection failed: {str(e)}"
        )


def _compute_distribution(
    dataset: Dataset,
    dimension: str,
    config: Config,
) -> Dict[int, float]:
    """
    Compute normalized score distribution for a dimension.
    Applies Laplace smoothing to avoid zero-probability.
    """

    counts = {
        score: 1  # Laplace smoothing
        for score in range(config.score_min, config.score_max + 1)
    }

    for entry in dataset:
        score = entry.scores[dimension]
        counts[score] += 1

    total = sum(counts.values())

    return {
        score: count / total
        for score, count in counts.items()
    }


def _kl_divergence(
    p: Dict[int, float],
    q: Dict[int, float],
) -> float:
    """
    Compute KL divergence D(P || Q).
    """

    kl = 0.0

    for key in p:
        kl += p[key] * math.log(p[key] / q[key])

    return kl
