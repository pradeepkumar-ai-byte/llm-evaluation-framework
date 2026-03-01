"""
Failure Analysis Layer

Author: Pradeep Kumar

Identifies weakest-performing dimensions and ranked failure patterns.
"""

from typing import Dict, List, Tuple, Any

from .models import Dataset
from .config import Config
from .utils import mean
from .exceptions import StatisticalComputationError


def analyze_failures(
    dataset: Dataset,
    config: Config,
) -> Dict[str, Any]:

    try:
        dimension_scores: Dict[str, List[int]] = {
            dim: [] for dim in config.required_dimensions
        }

        for entry in dataset:
            for dim in config.required_dimensions:
                dimension_scores[dim].append(
                    entry.scores[dim]
                )

        dimension_means: Dict[str, float] = {}
        failure_rates: Dict[str, float] = {}

        for dim, scores in dimension_scores.items():
            float_scores: List[float] = [float(s) for s in scores]

            dimension_means[dim] = mean(float_scores)

            failures = sum(
                1 for s in scores if s == config.score_min
            )

            failure_rates[dim] = failures / len(scores)

        ranked_dimensions: List[Tuple[str, float]] = sorted(
            dimension_means.items(),
            key=lambda x: x[1],
        )

        flagged_dimensions: List[str] = [
            dim
            for dim, rate in failure_rates.items()
            if rate > 0.5
        ]

        return {
            "dimension_means": dimension_means,
            "ranked_dimensions": ranked_dimensions,
            "failure_rates": failure_rates,
            "flagged_dimensions": flagged_dimensions,
        }

    except Exception as e:
        raise StatisticalComputationError(
            f"Failure analysis failed: {str(e)}"
        )