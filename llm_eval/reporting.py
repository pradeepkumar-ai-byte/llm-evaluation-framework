"""
Reporting module for generating evaluation summaries
"""

from datetime import datetime
from typing import List, Dict
from .config import CRITERIA


def calculate_averages(data: List[Dict]) -> Dict[str, float]:
    """
    Calculate average score per criterion.
    """
    totals = {criterion: 0 for criterion in CRITERIA}
    count = len(data)

    for item in data:
        for criterion in CRITERIA:
            totals[criterion] += item["label"][criterion]

    return {c: totals[c] / count for c in CRITERIA}


def generate_console_report(data: List[Dict], averages: Dict[str, float]) -> None:
    """
    Print professional summary report to console.
    """

    print("\n" + "=" * 60)
    print("LLM EVALUATION SUMMARY REPORT")
    print("=" * 60)
    print(f"Dataset size: {len(data)} items")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    for criterion in CRITERIA:
        readable = criterion.replace("_", " ").title()
        print(f"{readable:25}: {averages[criterion]:.2f} / 2.00")

    overall = sum(averages.values()) / len(CRITERIA)

    print("-" * 60)
    print(f"{'Overall Average':25}: {overall:.2f} / 2.00")
    print("=" * 60 + "\n")

    # Rank items
    ranked = [
        (index, sum(item["label"].values()) / len(CRITERIA))
        for index, item in enumerate(data)
    ]

    ranked.sort(key=lambda x: x[1], reverse=True)

    print("Top 3 Best Performing Items:")
    for idx, score in ranked[:3]:
        print(f"  Item {idx} — Avg: {score:.2f}")

    print("\nBottom 3 Worst Performing Items:")
    for idx, score in ranked[-3:]:
        print(f"  Item {idx} — Avg: {score:.2f}")

    print()
