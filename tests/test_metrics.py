"""
Тесты для модуля метрик читабельности.
"""

import pytest
from src.metrics import (
    count_syllables,
    count_syllables_ru,
    flesch_reading_ease,
    flesch_kincaid_grade,
    coleman_liau_index,
    automated_readability_index,
    smog_index,
    get_grade_description
)


class TestCountSyllables:
    """Тесты для функции подсчёта слогов (английский)."""
    
    def test_single_syllable_words(self):
        """Тест односложных слов."""
        assert count_syllables("cat") == 1
        assert count_syllables("dog") == 1
        assert count_syllables("run") == 1
        assert count_syllables("the") == 1
    
    def test_two_syllable_words(self):
        """Тест двусложных слов."""
        assert count_syllables("hello") == 2
        assert count_syllables("water") == 2
        assert count_syllables("happy") == 2
    
    def test_multi_syllable_words(self):
        """Тест многосложных слов."""
        assert count_syllables("beautiful") == 3
        assert count_syllables("education") == 4
        assert count_syllables("university") == 5
    
    def test_silent_e(self):
        """Тест слов с немой 'e'."""
        assert count_syllables("make") == 1
        assert count_syllables("time") == 1
        assert count_syllables("love") == 1
    
    def test_empty_string(self):
        """Тест пустой строки."""
        assert count_syllables("") == 0
    
    def test_minimum_one_syllable(self):
        """Минимум один слог для любого слова."""
        assert count_syllables("x") == 1
        assert count_syllables("by") == 1


class TestCountSyllablesRu:
    """Тесты для функции подсчёта слогов (русский)."""
    
    def test_single_syllable_words(self):
        """Тест односложных слов."""
        assert count_syllables_ru("мир") == 1
        assert count_syllables_ru("дом") == 1
        assert count_syllables_ru("кот") == 1
    
    def test_two_syllable_words(self):
        """Тест двусложных слов."""
        assert count_syllables_ru("мама") == 2
        assert count_syllables_ru("папа") == 2
        assert count_syllables_ru("привет") == 2
    
    def test_multi_syllable_words(self):
        """Тест многосложных слов."""
        assert count_syllables_ru("образование") == 6
        assert count_syllables_ru("университет") == 5
        assert count_syllables_ru("программирование") == 7
    
    def test_empty_string(self):
        """Тест пустой строки."""
        assert count_syllables_ru("") == 0


class TestFleschReadingEase:
    """Тесты для индекса Флеша."""
    
    def test_zero_words_returns_zero(self):
        """При нуле слов возвращает 0."""
        assert flesch_reading_ease(0, 1, 0) == 0.0
    
    def test_zero_sentences_returns_zero(self):
        """При нуле предложений возвращает 0."""
        assert flesch_reading_ease(10, 0, 15) == 0.0
    
    def test_simple_text_high_score(self):
        """Простой текст должен иметь высокий индекс."""
        # 20 слов, 4 предложения, 25 слогов
        score = flesch_reading_ease(20, 4, 25)
        assert score >= 70, f"Expected >= 70, got {score}"
    
    def test_complex_text_low_score(self):
        """Сложный текст должен иметь низкий индекс."""
        # 50 слов, 2 предложения, 120 слогов (много длинных слов)
        score = flesch_reading_ease(50, 2, 120)
        assert score < 50, f"Expected < 50, got {score}"
    
    def test_score_in_valid_range(self):
        """Индекс должен быть в диапазоне 0-100."""
        score = flesch_reading_ease(100, 5, 150)
        assert 0 <= score <= 100
    
    def test_typical_values(self):
        """Тест типичных значений."""
        # Средний текст
        score = flesch_reading_ease(100, 6, 140)
        assert 40 <= score <= 80


class TestFleschKincaidGrade:
    """Тесты для уровня класса по Флешу-Кинкейду."""
    
    def test_zero_values(self):
        """При нулевых значениях возвращает 0."""
        assert flesch_kincaid_grade(0, 0, 0) == 0.0
    
    def test_returns_grade_level(self):
        """Должен возвращать разумный уровень класса."""
        grade = flesch_kincaid_grade(100, 5, 150)
        assert 0 <= grade <= 20


class TestColemanLiauIndex:
    """Тесты для индекса Коулмана-Лиау."""
    
    def test_zero_words_returns_zero(self):
        """При нуле слов возвращает 0."""
        assert coleman_liau_index(0, 0, 1) == 0.0
    
    def test_returns_grade_level(self):
        """Должен возвращать уровень класса."""
        grade = coleman_liau_index(500, 100, 5)
        assert 0 <= grade <= 20
    
    def test_simple_text(self):
        """Простой текст должен иметь низкий уровень."""
        # Короткие слова, много предложений
        grade = coleman_liau_index(300, 100, 20)
        assert grade < 10


class TestAutomatedReadabilityIndex:
    """Тесты для ARI."""
    
    def test_zero_values(self):
        """При нулевых значениях возвращает 0."""
        assert automated_readability_index(0, 0, 0) == 0.0
    
    def test_returns_grade_level(self):
        """Должен возвращать уровень класса."""
        ari = automated_readability_index(500, 100, 5)
        assert ari > 0
    
    def test_simple_text_low_ari(self):
        """Простой текст должен иметь низкий ARI."""
        # 4 буквы на слово, 10 слов на предложение
        ari = automated_readability_index(400, 100, 10)
        assert ari < 10


class TestSmogIndex:
    """Тесты для индекса SMOG."""
    
    def test_zero_sentences(self):
        """При нуле предложений возвращает 0."""
        assert smog_index(10, 0) == 0.0
    
    def test_returns_grade_level(self):
        """Должен возвращать уровень класса."""
        grade = smog_index(30, 10)
        assert grade > 0


class TestGetGradeDescription:
    """Тесты для описания уровня сложности."""
    
    def test_elementary_level(self):
        """Уровень начальной школы."""
        level, audience = get_grade_description(3)
        assert "легко" in level.lower() or "начальн" in audience.lower()
    
    def test_university_level(self):
        """Университетский уровень."""
        level, audience = get_grade_description(14)
        assert "бакалавр" in audience.lower() or "сложно" in level.lower()