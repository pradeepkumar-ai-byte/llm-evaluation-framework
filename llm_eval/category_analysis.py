"""
Category-Level Performance Analysis
"""

from collections import defaultdict
from .config import CRITERIA


def compute_category_performance(dataset):
    category_scores = defaultdict(lambda: {c: [] for c in CRITERIA})

    for item in dataset:
        category = item.get("category", "uncategorized")
        for c in CRITERIA:
            category_scores[category][c].append(item["label"][c])

    # Compute averages
    category_averages = {}

    for category, scores in category_scores.items():
        category_averages[category] = {
            c: sum(scores[c]) / len(scores[c])
            for c in CRITERIA
        }

    return category_averages
