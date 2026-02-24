"""
Dataset Validation Layer

Author: Pradeep Kumar

This module enforces strict schema and integrity guarantees
for LLM evaluation datasets.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from .config import Config
from .models import EvaluationEntry, Metadata, Dataset
from .exceptions import DatasetValidationError


def load_and_validate_dataset(path: Path, config: Config) -> Dataset:
    """
    Load dataset from JSON file and perform full validation.
    """

    if not path.exists():
        raise DatasetValidationError(f"Dataset file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not isinstance(raw_data, list):
        raise DatasetValidationError("Dataset must be a list of entries.")

    if len(raw_data) < config.min_dataset_size:
        raise DatasetValidationError(
            f"Dataset must contain at least {config.min_dataset_size} entries."
        )

    entries: List[EvaluationEntry] = []
    seen_ids = set()
    group_counts: Dict[str, int] = {}

    for item in raw_data:
        entry = _validate_entry(item, config)

        if entry.id in seen_ids:
            raise DatasetValidationError(
                f"Duplicate ID detected: {entry.id}"
            )
        seen_ids.add(entry.id)

        group_counts[entry.metadata.group] = (
            group_counts.get(entry.metadata.group, 0) + 1
        )

        entries.append(entry)

    _validate_group_integrity(group_counts)

    return entries


def _validate_entry(item: Dict, config: Config) -> EvaluationEntry:
    required_fields = {"id", "prompt", "response", "scores", "metadata"}

    if not required_fields.issubset(item.keys()):
        raise DatasetValidationError(
            f"Missing required fields. Required: {required_fields}"
        )

    scores = item["scores"]
    _validate_scores(scores, config)

    metadata = item["metadata"]
    _validate_metadata(metadata)

    return EvaluationEntry(
        id=item["id"],
        prompt=item["prompt"],
        response=item["response"],
        scores=scores,
        metadata=Metadata(
            model=metadata["model"],
            timestamp=metadata["timestamp"],
            group=metadata["group"],
        ),
    )


def _validate_scores(scores: Dict[str, int], config: Config) -> None:
    if not isinstance(scores, dict):
        raise DatasetValidationError("Scores must be a dictionary.")

    required = set(config.required_dimensions)
    provided = set(scores.keys())

    if required != provided:
        raise DatasetValidationError(
            f"Score dimensions mismatch. Required: {required}"
        )

    for dimension, value in scores.items():
        if not isinstance(value, int):
            raise DatasetValidationError(
                f"Score for '{dimension}' must be integer."
            )
        if not (config.score_min <= value <= config.score_max):
            raise DatasetValidationError(
                f"Score for '{dimension}' must be between "
                f"{config.score_min} and {config.score_max}."
            )


def _validate_metadata(metadata: Dict) -> None:
    required_fields = {"model", "timestamp", "group"}

    if not required_fields.issubset(metadata.keys()):
        raise DatasetValidationError(
            f"Metadata missing required fields: {required_fields}"
        )

    try:
        datetime.fromisoformat(metadata["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        raise DatasetValidationError(
            f"Invalid ISO 8601 timestamp: {metadata['timestamp']}"
        )


def _validate_group_integrity(group_counts: Dict[str, int]) -> None:
    """
    Ensures at least two groups exist and
    each group contains at least 2 samples for statistical testing.
    """
    if len(group_counts) < 2:
        raise DatasetValidationError(
            "At least two groups are required for statistical comparison."
        )

    for group, count in group_counts.items():
        if count < 2:
            raise DatasetValidationError(
                f"Group '{group}' must contain at least 2 entries."
    )
