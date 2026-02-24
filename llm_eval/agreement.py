"""
Inter-Rater Agreement Layer

Author: Pradeep Kumar

Implements Cohen's Kappa for inter-rater reliability.
"""

from typing import Dict, List
from collections import defaultdict

from .models import Dataset
from .config import Config
from .exceptions import StatisticalComputationError


def compute_cohens_kappa(
    dataset: Dataset,
    config: Config,
) -> Dict[str, float]:
    """
    Compute Cohen's Kappa per dimension.
    Assumes exactly two raters (groups) scoring same IDs.
    """

    try:
        paired_entries = _pair_by_id(dataset)

        kappa_results: Dict[str, float] = {}

        for dimension in config.required_dimensions:
            rater_a_scores = []
            rater_b_scores = []

            for pair in paired_entries.values():
                rater_a_scores.append(pair[0].scores[dimension])
                rater_b_scores.append(pair[1].scores[dimension])

            kappa = _cohens_kappa(rater_a_scores, rater_b_scores)
            kappa_results[dimension] = kappa

        return kappa_results

    except Exception as e:
        raise StatisticalComputationError(
            f"Cohen's Kappa computation failed: {str(e)}"
        )


def _pair_by_id(dataset: Dataset):
    """
    Group entries by ID and ensure exactly two ratings per ID.
    """

    grouped = defaultdict(list)

    for entry in dataset:
        grouped[entry.id].append(entry)

    for entry_id, entries in grouped.items():
        if len(entries) != 2:
            raise StatisticalComputationError(
                f"ID {entry_id} must have exactly 2 ratings."
            )

    return grouped


def _cohens_kappa(
    rater_a: List[int],
    rater_b: List[int],
) -> float:
    """
    Compute Cohen's Kappa.
    """

    if len(rater_a) != len(rater_b):
        raise StatisticalComputationError(
            "Rater score lengths mismatch."
        )

    n = len(rater_a)

    observed_agreement = sum(
        1 for a, b in zip(rater_a, rater_b) if a == b
    ) / n

    categories = set(rater_a) | set(rater_b)

    prob_a = {
        c: rater_a.count(c) / n for c in categories
    }
    prob_b = {
        c: rater_b.count(c) / n for c in categories
    }

    expected_agreement = sum(
        prob_a[c] * prob_b[c] for c in categories
    )

    if expected_agreement == 1:
        return 1.0

    return (observed_agreement - expected_agreement) / (
        1 - expected_agreement
      )
