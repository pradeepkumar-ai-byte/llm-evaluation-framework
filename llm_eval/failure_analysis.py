"""
Failure taxonomy analysis module.
Categorizes hard failures (score = 0).
"""

from typing import List, Dict
from .config import CRITERIA


def categorize_failures(data: List[Dict]) -> Dict:
    summary = {
        "instruction_failures": 0,
        "factual_errors": 0,
        "logic_breakdowns": 0,
        "safety_violations": 0,
        "tone_mismatches": 0,
        "total_failed_samples": 0
    }

    for item in data:
        failed = [c for c in CRITERIA if item["label"][c] == 0]

        if not failed:
            continue

        summary["total_failed_samples"] += 1

        for criterion in failed:
            if criterion == "instruction_adherence":
                summary["instruction_failures"] += 1
            elif criterion == "factual_accuracy":
                summary["factual_errors"] += 1
            elif criterion == "logical_coherence":
                summary["logic_breakdowns"] += 1
            elif criterion == "safety":
                summary["safety_violations"] += 1
            elif criterion == "tone_alignment":
                summary["tone_mismatches"] += 1

    return summary
