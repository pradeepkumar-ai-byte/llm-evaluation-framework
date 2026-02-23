"""
Main scoring engine for LLM Evaluation Framework
"""

import json
import argparse
import sys
from pathlib import Path

from .validation import validate_dataset
from .reporting import calculate_averages, generate_console_report


def load_dataset(path: str):
    """
    Load dataset JSON file safely.
    """
    file_path = Path(path)

    if not file_path.exists():
        print(f"❌ Dataset file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌
