"""
LLM Evaluation Framework - Core Package
"""

__version__ = "2.0.0"
__author__ = "Pradeep Kumar"

from .config import CRITERIA
from .validation import validate_data
from .reporting import compute_statistics, generate_console_report
from .failure_analysis import categorize_failures
from .export import export_json, export_csv

__all__ = [
    "CRITERIA",
    "validate_data",
    "compute_statistics",
    "generate_console_report",
    "categorize_failures",
    "export_json",
    "export_csv"
]
