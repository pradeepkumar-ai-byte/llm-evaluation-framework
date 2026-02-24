#!/usr/bin/env python3
"""
LLM Evaluation Framework – Elite Professional Runner

Pipeline:
1. Load dataset
2. Validate structure
3. Compute statistics
4. Analyze failure taxonomy
5. Compute category performance
6. Generate console report
7. Export JSON + CSV reports
"""

import sys
import json
from pathlib import Path

from llm_eval.validation import validate_data
from llm_eval.reporting import compute_statistics, generate_console_report
from llm_eval.failure_analysis import categorize_failures
from llm_eval.category_analysis import compute_category_performance
from llm_eval.export import export_json, export_csv


DATA_PATH = Path("llm_eval/dataset.json")


def load_dataset(path: Path):
    if not path.exists():
        print(f"❌ Dataset not found at {path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        sys.exit(1)


def main():
    print("\n" + "=" * 70)
    print("LLM EVALUATION FRAMEWORK – ELITE EDITION")
    print("=" * 70)

    # 1️⃣ Load dataset
    dataset = load_dataset(DATA_PATH)

    # 2️⃣ Validate structure
    validate_data(dataset)

    # 3️⃣ Compute statistics
    stats = compute_statistics(dataset)

    # 4️⃣ Failure analysis
    failure_summary = categorize_failures(dataset)

    # 5️⃣ Category performance
    category_stats = compute_category_performance(dataset)

    # 6️⃣ Console report
    generate_console_report(dataset, stats)

    # 🔎 Failure Diagnostics
    print("\n" + "=" * 70)
    print("FAILURE DIAGNOSTIC SUMMARY")
    print("=" * 70)

    for key, value in failure_summary.items():
        print(f"{key.replace('_', ' ').title():30}: {value}")

    # 📊 Category Analytics
    print("\n" + "=" * 70)
    print("CATEGORY PERFORMANCE ANALYSIS")
    print("=" * 70)

    for category, scores in category_stats.items():
        print(f"\nCategory: {category}")
        for criterion, avg in scores.items():
            print(f"  {criterion.replace('_',' ').title():25}: {avg:.2f}")

    # 7️⃣ Export Reports
    json_path = export_json(dataset, stats, failure_summary)
    csv_path = export_csv(dataset)

    print("\n" + "=" * 70)
    print("EXPORT COMPLETE")
    print("=" * 70)
    print(f"JSON report saved to: {json_path}")
    print(f"CSV export saved to: {csv_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
