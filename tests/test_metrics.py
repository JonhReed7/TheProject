"""Тесты для модуля метрик."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.metrics import (
    count_syllables,
    count_syllables_ru,
    flesch_reading_ease,
    coleman_liau_index,
    automated_readability_index
)


class TestCountSyllables:
    """Тесты подсчёта слогов."""
    
    def test_simple_words(self):
        """Тест простых слов."""
        assert count_syllables("cat") == 1
        assert count_syllables("hello") == 2
    
    def test_empty_string(self):
        """Тест пустой строки."""
        assert count_syllables("") == 0
    
    def test_minimum_one(self):
        """Минимум один слог."""
        assert count_syllables("a") >= 1


class TestCountSyllablesRu:
    """Тесты подсчёта слогов (русский)."""
    
    def test_russian_words(self):
        """Тест русских слов."""
        assert count_syllables_ru("мама") == 2
        assert count_syllables_ru("дом") == 1
    
    def test_empty_string(self):
        """Тест пустой строки."""
        assert count_syllables_ru("") == 0


class TestFleschReadingEase:
    """Тесты индекса Флеша."""
    
    def test_zero_words(self):
        """При нуле слов возвращает 0."""
        result = flesch_reading_ease(0, 1, 0)
        assert result == 0.0
    
    def test_zero_sentences(self):
        """При нуле предложений возвращает 0."""
        result = flesch_reading_ease(10, 0, 15)
        assert result == 0.0
    
    def test_returns_number(self):
        """Возвращает число."""
        result = flesch_reading_ease(100, 5, 150)
        assert isinstance(result, float)
        assert 0 <= result <= 100


class TestColemanLiauIndex:
    """Тесты индекса Коулмана-Лиау."""
    
    def test_zero_words(self):
        """При нуле слов возвращает 0."""
        result = coleman_liau_index(0, 0, 1)
        assert result == 0.0
    
    def test_returns_number(self):
        """Возвращает число."""
        result = coleman_liau_index(500, 100, 5)
        assert isinstance(result, float)
        assert result >= 0


class TestARI:
    """Тесты ARI."""
    
    def test_zero_values(self):
        """При нулевых значениях возвращает 0."""
        result = automated_readability_index(0, 0, 0)
        assert result == 0.0
    
    def test_returns_number(self):
        """Возвращает число."""
        result = automated_readability_index(400, 100, 5)
        assert isinstance(result, float)
        assert result >= 0