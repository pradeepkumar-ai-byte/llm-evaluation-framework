"""
Advanced Reporting Module for LLM Evaluation Framework
Elite Statistical Edition
"""

from datetime import datetime
from typing import List, Dict
from statistics import mean, stdev
from collections import Counter
from .config import CRITERIA


def compute_statistics(data: List[Dict]) -> Dict:
    stats = {}

    for criterion in CRITERIA:
        scores = [item["label"][criterion] for item in data]

        stats[criterion] = {
            "mean": mean(scores),
            "std_dev": stdev(scores) if len(scores) > 1 else 0.0,
            "failure_rate": scores.count(0) / len(scores),
            "perfect_rate": scores.count(2) / len(scores),
            "distribution": dict(Counter(scores))
        }

    return stats


def generate_console_report(data: List[Dict], stats: Dict) -> None:
    print("\n" + "=" * 70)
    print("LLM EVALUATION – ADVANCED ANALYTICS REPORT")
    print("=" * 70)
    print(f"Dataset size: {len(data)} items")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    overall_means = []

    for criterion, values in stats.items():
        readable = criterion.replace("_", " ").title()

        overall_means.append(values["mean"])

        print(f"{readable}")
        print(f"  Mean Score     : {values['mean']:.2f}")
        print(f"  Std Deviation  : {values['std_dev']:.2f}")
        print(f"  Failure Rate   : {values['failure_rate']:.2%}")
        print(f"  Perfect Rate   : {values['perfect_rate']:.2%}")
        print(f"  Distribution   : {values['distribution']}")
        print()

    overall_avg = mean(overall_means)

    print("-" * 70)
    print(f"Overall Model Quality Score: {overall_avg:.2f} / 2.00")
    print("=" * 70 + "\n")
