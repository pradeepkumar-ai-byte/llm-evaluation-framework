"""
Dataset validation module.
Ensures dataset structure and scoring integrity.
"""

import sys
from typing import List, Dict
from .config import CRITERIA, MIN_SCORE, MAX_SCORE


def validate_data(data: List[Dict]) -> None:
    if not isinstance(data, list):
        print("Dataset must be a list of items.", file=sys.stderr)
        sys.exit(1)

    for index, item in enumerate(data):

        if "prompt" not in item or "response" not in item:
            print(f"Item {index} missing 'prompt' or 'response'.", file=sys.stderr)
            sys.exit(1)

        if "label" not in item:
            print(f"Item {index} missing 'label'.", file=sys.stderr)
            sys.exit(1)

        label = item["label"]

        for criterion in CRITERIA:
            if criterion not in label:
                print(f"Item {index} missing criterion '{criterion}'.", file=sys.stderr)
                sys.exit(1)

            score = label[criterion]

            if not isinstance(score, int):
                print(f"Item {index} criterion '{criterion}' must be integer.", file=sys.stderr)
                sys.exit(1)

            if score < MIN_SCORE or score > MAX_SCORE:
                print(
                    f"Item {index} criterion '{criterion}' must be between {MIN_SCORE} and {MAX_SCORE}.",
                    file=sys.stderr
                )
                sys.exit(1)
