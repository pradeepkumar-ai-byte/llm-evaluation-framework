"""
Benchmarking Layer

Author: Pradeep Kumar

Compares evaluation dataset against a reference dataset.
"""

from typing import Dict, List

from .models import Dataset
from .config import Config
from .utils import mean
from .exceptions import StatisticalComputationError


def benchmark_against_reference(
    dataset: Dataset,
    reference_dataset: Dataset,
    config: Config,
) -> Dict[str, object]:
    """
    Compare dataset against reference dataset.

    Returns:
        {
            "dimension_deltas": {...},
            "overall_delta": float,
            "improved_dimensions": [...],
            "declined_dimensions": [...]
        }
    """

    try:
        current_means = _compute_dimension_means(dataset, config)
        reference_means = _compute_dimension_means(
            reference_dataset,
            config,
        )

        dimension_deltas: Dict[str, float] = {}

        for dim in config.required_dimensions:
            delta = current_means[dim] - reference_means[dim]
            dimension_deltas[dim] = delta

        overall_current = mean(current_means.values())
        overall_reference = mean(reference_means.values())
        overall_delta = overall_current - overall_reference

        improved_dimensions = [
            dim for dim, delta in dimension_deltas.items()
            if delta > 0
        ]

        declined_dimensions = [
            dim for dim, delta in dimension_deltas.items()
            if delta < 0
        ]

        return {
            "dimension_deltas": dimension_deltas,
            "overall_delta": overall_delta,
            "improved_dimensions": improved_dimensions,
            "declined_dimensions": declined_dimensions,
        }

    except Exception as e:
        raise StatisticalComputationError(
            f"Benchmark computation failed: {str(e)}"
        )


def _compute_dimension_means(
    dataset: Dataset,
    config: Config,
) -> Dict[str, float]:

    dimension_scores: Dict[str, List[int]] = {
        dim: [] for dim in config.required_dimensions
    }

    for entry in dataset:
        for dim in config.required_dimensions:
            dimension_scores[dim].append(
                entry.scores[dim]
            )

    return {
        dim: mean(scores)
        for dim, scores in dimension_scores.items()
      }
