"""
Text Readability Analyzer
=========================

Инструмент для анализа читабельности учебных материалов.

Основные компоненты:
- TextAnalyzer: главный класс для анализа текста
- ReadabilityResult: результат анализа с метриками
- Функции расчёта индексов читабельности
"""

from .analyzer import TextAnalyzer, ReadabilityResult
from .metrics import (
    flesch_reading_ease,
    coleman_liau_index,
    automated_readability_index,
    count_syllables,
    count_syllables_ru
)

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = [
    "TextAnalyzer",
    "ReadabilityResult",
    "flesch_reading_ease",
    "coleman_liau_index",
    "automated_readability_index",
    "count_syllables",
    "count_syllables_ru",
]