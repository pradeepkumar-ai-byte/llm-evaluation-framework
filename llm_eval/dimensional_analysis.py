"""
Dimensional Analysis Layer

Author: Pradeep Kumar

Provides advanced per-dimension statistical diagnostics.
"""

from typing import Dict, List

from .models import Dataset
from .config import Config
from .utils import mean, variance, standard_deviation
from .exceptions import StatisticalComputationError


def dimensional_breakdown(
    dataset: Dataset,
    config: Config,
) -> Dict[str, object]:
    """
    Perform detailed per-dimension statistical analysis.

    Returns:
        {
            "dimension_statistics": {
                dimension: {
                    "mean": float,
                    "variance": float,
                    "std_dev": float,
                    "coefficient_of_variation": float
                }
            },
            "high_variance_dimensions": [...]
        }
    """

    try:
        dimension_scores: Dict[str, List[int]] = {
            dim: [] for dim in config.required_dimensions
        }

        for entry in dataset:
            for dim in config.required_dimensions:
                dimension_scores[dim].append(
                    entry.scores[dim]
                )

        dimension_statistics: Dict[str, Dict[str, float]] = {}
        high_variance_dimensions = []

        for dim, scores in dimension_scores.items():
            m = mean(scores)
            var = variance(scores)
            sd = standard_deviation(scores)

            if m == 0:
                cv = 0.0
            else:
                cv = sd / m

            dimension_statistics[dim] = {
                "mean": m,
                "variance": var,
                "std_dev": sd,
                "coefficient_of_variation": cv,
            }

            if cv > 0.5:
                high_variance_dimensions.append(dim)

        return {
            "dimension_statistics": dimension_statistics,
            "high_variance_dimensions": high_variance_dimensions,
        }

    except Exception as e:
        raise StatisticalComputationError(
            f"Dimensional analysis failed: {str(e)}"
          )
