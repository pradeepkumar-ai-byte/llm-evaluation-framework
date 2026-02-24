import pytest
from pathlib import Path
import json
import tempfile

from llm_eval.config import Config
from llm_eval.validation import load_and_validate_dataset
from llm_eval.exceptions import DatasetValidationError


def create_valid_dataset():
    return [
        {
            "id": 1,
            "prompt": "Test",
            "response": "Test",
            "scores": {
                "instruction_adherence": 2,
                "factual_accuracy": 2,
                "logical_coherence": 2,
                "safety": 2,
                "tone_alignment": 2,
            },
            "metadata": {
                "model": "gpt-4",
                "timestamp": "2026-02-24T10:15:30Z",
                "group": "A",
            },
        },
        {
            "id": 1,
            "prompt": "Test",
            "response": "Test",
            "scores": {
                "instruction_adherence": 1,
                "factual_accuracy": 1,
                "logical_coherence": 1,
                "safety": 1,
                "tone_alignment": 1,
            },
            "metadata": {
                "model": "gpt-4",
                "timestamp": "2026-02-24T10:15:30Z",
                "group": "B",
            },
        },
    ]


def test_valid_dataset_passes():
    config = Config(min_dataset_size=2)
    data = create_valid_dataset()

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = Path(tmp.name)

    dataset = load_and_validate_dataset(tmp_path, config)
    assert len(dataset) == 2


def test_duplicate_id_fails():
    config = Config(min_dataset_size=2)
    data = create_valid_dataset()
    data[1]["id"] = 2

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = Path(tmp.name)

    with pytest.raises(DatasetValidationError):
        load_and_validate_dataset(tmp_path, config)
