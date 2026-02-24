"""
Configuration module for LLM Evaluation Framework
Defines evaluation criteria and scoring boundaries.
"""

CRITERIA = [
    "instruction_adherence",
    "factual_accuracy",
    "logical_coherence",
    "safety",
    "tone_alignment"
]

MIN_SCORE = 0
MAX_SCORE = 2
