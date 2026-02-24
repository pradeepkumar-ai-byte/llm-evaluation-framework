from llm_eval.config import Config
from llm_eval.models import EvaluationEntry, Metadata
from llm_eval.significance import independent_t_test
from llm_eval.agreement import compute_cohens_kappa


def create_dataset():
    return [
        EvaluationEntry(
            id=1,
            prompt="P",
            response="R",
            scores={
                "instruction_adherence": 2,
                "factual_accuracy": 2,
                "logical_coherence": 2,
                "safety": 2,
                "tone_alignment": 2,
            },
            metadata=Metadata(
                model="gpt-4",
                timestamp="2026-02-24T10:15:30Z",
                group="A",
            ),
        ),
        EvaluationEntry(
            id=1,
            prompt="P",
            response="R",
            scores={
                "instruction_adherence": 1,
                "factual_accuracy": 1,
                "logical_coherence": 1,
                "safety": 1,
                "tone_alignment": 1,
            },
            metadata=Metadata(
                model="gpt-4",
                timestamp="2026-02-24T10:15:30Z",
                group="B",
            ),
        ),
    ]


def test_t_test_runs():
    config = Config(min_dataset_size=2)
    dataset = create_dataset()
    result = independent_t_test(dataset, config)

    assert "t_statistic" in result


def test_kappa_runs():
    config = Config(min_dataset_size=2)
    dataset = create_dataset()
    result = compute_cohens_kappa(dataset, config)

    assert "instruction_adherence" in result
