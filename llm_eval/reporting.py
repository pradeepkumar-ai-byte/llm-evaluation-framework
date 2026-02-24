"""
Reporting Layer

Author: Pradeep Kumar

Generates deterministic statistical summaries for evaluation datasets.
"""

from typing import Dict, List

from .config import Config
from .models import Dataset
from .utils import mean, standard_deviation, confidence_interval
from .exceptions import StatisticalComputationError


def generate_report(dataset: Dataset, config: Config) -> str:
    """
    Generate a formatted statistical summary report.
    """

    try:
        dimension_scores = _collect_dimension_scores(dataset, config)

        report_lines: List[str] = []
        report_lines.append("LLM Evaluation Report")
        report_lines.append("-" * 30)

        overall_scores = []

        for dimension, scores in dimension_scores.items():
            m = mean(scores)
            sd = standard_deviation(scores)
            ci = confidence_interval(scores, config.confidence_level)

            overall_scores.extend(scores)

            report_lines.append(f"\nDimension: {dimension}")
            report_lines.append(f"  Mean: {m:.4f}")
            report_lines.append(f"  Std Dev: {sd:.4f}")
            report_lines.append(f"  95% CI Margin: ±{ci:.4f}")

        overall_mean = mean(overall_scores)
        overall_sd = standard_deviation(overall_scores)
        overall_ci = confidence_interval(
            overall_scores,
            config.confidence_level,
        )

        report_lines.append("\nOverall Summary")
        report_lines.append(f"  Overall Mean: {overall_mean:.4f}")
        report_lines.append(f"  Overall Std Dev: {overall_sd:.4f}")
        report_lines.append(f"  Overall 95% CI Margin: ±{overall_ci:.4f}")

        return "\n".join(report_lines)

    except Exception as e:
        raise StatisticalComputationError(
            f"Reporting computation failed: {str(e)}"
        )


def _collect_dimension_scores(
    dataset: Dataset,
    config: Config,
) -> Dict[str, List[int]]:
    """
    Collect per-dimension score lists from dataset.
    """

    dimension_scores: Dict[str, List[int]] = {
        dim: [] for dim in config.required_dimensions
    }

    for entry in dataset:
        for dimension in config.required_dimensions:
            dimension_scores[dimension].append(
                entry.scores[dimension]
            )

    return dimension_scores
