"""Тесты для модуля метрик."""
import pytest
from src.metrics import (
    count_syllables,
    count_syllables_ru,
    flesch_reading_ease,
    coleman_liau_index,
    automated_readability_index
)


class TestSyllableCount:
    """Тесты подсчёта слогов."""
    
    def test_simple_words(self):
        assert count_syllables("hello") == 2
        assert count_syllables("world") == 1
        assert count_syllables("beautiful") == 3
    
    def test_single_syllable(self):
        assert count_syllables("cat") == 1
        assert count_syllables("dog") == 1
    
    def test_russian_words(self):
        assert count_syllables_ru("привет") == 2
        assert count_syllables_ru("образование") == 6
        assert count_syllables_ru("мир") == 1


class TestFleschReadingEase:
    """Тесты индекса Флеша."""
    
    def test_zero_words(self):
        assert flesch_reading_ease(0, 1, 0) == 0.0
    
    def test_zero_sentences(self):
        assert flesch_reading_ease(10, 0, 15) == 0.0
    
    def test_simple_text(self):
        # Простой текст должен иметь высокий индекс
        score = flesch_reading_ease(
            total_words=20,
            total_sentences=4,
            total_syllables=25
        )
        assert 60 <= score <= 100
    
    def test_complex_text(self):
        # Сложный текст с длинными предложениями
        score = flesch_reading_ease(
            total_words=100,
            total_sentences=3,
            total_syllables=200
        )
        assert score < 50


class TestColemanLiauIndex:
    """Тесты индекса Коулмана-Лиау."""
    
    def test_zero_words(self):
        assert coleman_liau_index(0, 0, 1) == 0.0
    
    def test_returns_grade_level(self):
        grade = coleman_liau_index(
            total_chars=500,
            total_words=100,
            total_sentences=5
        )
        assert 0 <= grade <= 20


class TestARI:
    """Тесты автоматического индекса читабельности."""
    
    def test_zero_values(self):
        assert automated_readability_index(0, 0, 0) == 0.0
    
    def test_normal_text(self):
        ari = automated_readability_index(
            total_chars=400,
            total_words=100,
            total_sentences=5
        )
        assert ari > 0