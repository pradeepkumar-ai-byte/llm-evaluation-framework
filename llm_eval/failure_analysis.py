"""
Failure Analysis Module
Elite Diagnostic Layer
"""

from typing import List, Dict
from .config import CRITERIA


def categorize_failures(data: List[Dict]) -> Dict:
    failure_summary = {
        "instruction_failure": 0,
        "factual_error": 0,
        "logic_breakdown": 0,
        "safety_violation": 0,
        "tone_mismatch": 0,
        "multi_failure": 0,
        "total_failed_samples": 0
    }

    for item in data:
        failed_criteria = [
            criterion for criterion in CRITERIA
            if item["label"][criterion] == 0
        ]

        if not failed_criteria:
            continue

        failure_summary["total_failed_samples"] += 1

        if len(failed_criteria) > 1:
            failure_summary["multi_failure"] += 1

        for criterion in failed_criteria:
            if criterion == "instruction_adherence":
                failure_summary["instruction_failure"] += 1
            elif criterion == "factual_accuracy":
                failure_summary["factual_error"] += 1
            elif criterion == "logical_coherence":
                failure_summary["logic_breakdown"] += 1
            elif criterion == "safety":
                failure_summary["safety_violation"] += 1
            elif criterion == "tone_alignment":
                failure_summary["tone_mismatch"] += 1

    return failure_summary
