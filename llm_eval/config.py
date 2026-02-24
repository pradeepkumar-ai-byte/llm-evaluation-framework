from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Config:
    """
    Immutable configuration object for the LLM Evaluation Framework.
    """

    # Dataset validation
    min_dataset_size: int = 5
    score_min: int = 0
    score_max: int = 2

    # Statistical thresholds
    confidence_level: float = 0.95
    drift_threshold: float = 0.1
    significance_alpha: float = 0.05

    # Bootstrap configuration
    bootstrap_iterations: int = 1000
    random_seed: int = 42

    # Required score dimensions
    required_dimensions: Tuple[str, ...] = (
        "instruction_adherence",
        "factual_accuracy",
        "logical_coherence",
        "safety",
        "tone_alignment",
    )
