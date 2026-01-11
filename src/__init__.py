"""Text Readability Analyzer."""

from .analyzer import TextAnalyzer, ReadabilityResult
from .metrics import (
    flesch_reading_ease,
    coleman_liau_index,
    automated_readability_index,
    count_syllables,
    count_syllables_ru
)

__version__ = "1.0.0"
__all__ = [
    "TextAnalyzer",
    "ReadabilityResult",
    "flesch_reading_ease",
    "coleman_liau_index",
    "automated_readability_index",
    "count_syllables",
    "count_syllables_ru",
]