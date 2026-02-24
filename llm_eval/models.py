from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Metadata:
    model: str
    timestamp: str
    group: str


@dataclass(frozen=True)
class EvaluationEntry:
    id: int
    prompt: str
    response: str
    scores: Dict[str, int]
    metadata: Metadata


Dataset = List[EvaluationEntry]
