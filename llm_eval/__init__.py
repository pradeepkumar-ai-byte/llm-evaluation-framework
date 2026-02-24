"""
LLM Evaluation Framework – Core Package

This package provides modular components for:

- Dataset validation
- Statistical scoring
- Failure taxonomy analysis
- Category-level performance analytics
- Structured export utilities

Designed for research-grade LLM evaluation workflows.
"""

__version__ = "1.0.0"
__author__ = "Pradeep Kumar"

from .config import CRITERIA
from .validation import validate_data
from .reporting import compute_statistics, generate_console_report
from .failure_analysis import categorize_failures
from .category_analysis import compute_category_performance
from .export import export_json, export_csv

__all__ = [
    "CRITERIA",
    "validate_data",
    "compute_statistics",
    "generate_console_report",
    "categorize_failures",
    "compute_category_performance",
    "export_json",
    "export_csv",
]
