"""
Export Layer

Author: Pradeep Kumar

Handles structured result exporting.
"""

import json
from pathlib import Path
from typing import Dict, Any

from .exceptions import EvaluationError


def export_results(
    results: Dict[str, Any],
    output_path: Path,
) -> None:
    """
    Export evaluation results to JSON file.
    """

    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

    except Exception as e:
        raise EvaluationError(
            f"Failed to export results: {str(e)}"
        )
