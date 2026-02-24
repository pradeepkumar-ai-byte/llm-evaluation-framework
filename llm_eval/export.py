"""
Export module.
Supports JSON and CSV research-grade exports.
"""

import json
import csv
from datetime import datetime
from pathlib import Path


def export_json(dataset, stats, failure_summary, output_dir="reports"):
    Path(output_dir).mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(output_dir) / f"evaluation_report_{timestamp}.json"

    report = {
        "generated_at": timestamp,
        "dataset_size": len(dataset),
        "statistics": stats,
        "failure_summary": failure_summary,
        "samples": dataset
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return str(filename)


def export_csv(dataset, output_dir="reports"):
    Path(output_dir).mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(output_dir) / f"dataset_export_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "prompt",
            "instruction_adherence",
            "factual_accuracy",
            "logical_coherence",
            "safety",
            "tone_alignment"
        ])

        for item in dataset:
            writer.writerow([
                item["prompt"],
                item["label"]["instruction_adherence"],
                item["label"]["factual_accuracy"],
                item["label"]["logical_coherence"],
                item["label"]["safety"],
                item["label"]["tone_alignment"]
            ])

    return str(filename)
