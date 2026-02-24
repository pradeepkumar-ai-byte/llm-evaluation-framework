class EvaluationError(Exception):
    """Base exception for evaluation framework."""
    pass


class DatasetValidationError(EvaluationError):
    """Raised when dataset fails schema or integrity validation."""
    pass


class StatisticalComputationError(EvaluationError):
    """Raised when statistical computation fails."""
    pass


class DriftDetectionError(EvaluationError):
    """Raised when drift detection fails."""
    pass
