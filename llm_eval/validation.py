"""
Validation module for dataset integrity checks
"""

import sys
from typing import List, Dict
from .config import CRITERIA, MIN_SCORE, MAX_SCORE


def validate_dataset(data: List[Dict]) -> None:
    """
    Validates dataset structure and scoring integrity.
    Exits program if validation fails.
    """

    if not isinstance(data, list):
        print("❌ Dataset must be a list of items.", file=sys.stderr)
        sys.exit(1)

    for index, item in enumerate(data):

        if "prompt" not in item or "response" not in item:
            print(f"❌ Item {index} missing 'prompt' or 'response'.", file=sys.stderr)
            sys.exit(1)

        if "label" not in item:
            print(f"❌ Item {index} missing 'label'.", file=sys.stderr)
            sys.exit(1)

        label = item["label"]

        for criterion in CRITERIA:
            if criterion not in label:
                print(
                    f"❌ Item {index} missing criterion '{criterion}'.",
                    file=sys.stderr
                )
                sys.exit(1)

            score = label[criterion]

            if not isinstance(score, int):
                print(
                    f"❌ Item {index}, '{criterion}' must be integer.",
                    file=sys.stderr
                )
                sys.exit(1)

            if score < MIN_SCORE or score > MAX_SCORE:
                print(
                    f"❌ Item {index}, '{criterion}' score must be between {MIN_SCORE} and {MAX_SCORE}.",
                    file=sys.stderr
                )
                sys.exit(1)
