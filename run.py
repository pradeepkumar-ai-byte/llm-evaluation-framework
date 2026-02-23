"""
Root execution file for LLM Evaluation Framework
Professional Entry Point
"""

import json
import argparse
import sys
from pathlib import Path

from llm_eval.validation import validate_dataset
from llm_eval.reporting import calculate_averages, generate_console_report


def load_dataset(path: str):
    file_path = Path(path)

    if not file_path.exists():
        print(f"❌ Dataset file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Evaluation Framework – Professional Edition"
    )

    parser.add_argument(
        "--data",
        default="dataset.json",
        help="Path to dataset JSON file"
    )

    args = parser.parse_args()

    data = load_dataset(args.data)

    validate_dataset(data)

    averages = calculate_averages(data)

    generate_console_report(data, averages)


if __name__ == "__main__":
    main()
