"""Тесты для класса TextAnalyzer."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.analyzer import TextAnalyzer, ReadabilityResult


class TestTextAnalyzerInit:
    """Тесты инициализации."""
    
    def test_default_language(self):
        """По умолчанию язык auto."""
        analyzer = TextAnalyzer()
        assert analyzer.language == "auto"
    
    def test_english_language(self):
        """Установка английского."""
        analyzer = TextAnalyzer(language="en")
        assert analyzer.language == "en"
    
    def test_russian_language(self):
        """Установка русского."""
        analyzer = TextAnalyzer(language="ru")
        assert analyzer.language == "ru"


class TestTextAnalyzerAnalyze:
    """Тесты метода analyze."""
    
    def test_returns_result(self):
        """Возвращает ReadabilityResult."""
        analyzer = TextAnalyzer(language="en")
        text = "The cat sat on the mat. The dog ran in the park. Birds fly high."
        result = analyzer.analyze(text)
        assert isinstance(result, ReadabilityResult)
    
    def test_empty_text_error(self):
        """Пустой текст вызывает ошибку."""
        analyzer = TextAnalyzer()
        with pytest.raises(ValueError):
            analyzer.analyze("")
    
    def test_short_text_error(self):
        """Короткий текст вызывает ошибку."""
        analyzer = TextAnalyzer()
        with pytest.raises(ValueError):
            analyzer.analyze("Hello world.")
    
    def test_word_count_positive(self):
        """Количество слов положительное."""
        analyzer = TextAnalyzer()
        text = "This is a simple test. It has many words. We need at least ten words here."
        result = analyzer.analyze(text)
        assert result.word_count > 0
    
    def test_sentence_count_positive(self):
        """Количество предложений положительное."""
        analyzer = TextAnalyzer()
        text = "First sentence here. Second sentence here. Third sentence here now."
        result = analyzer.analyze(text)
        assert result.sentence_count > 0
    
    def test_flesch_score_valid(self):
        """Индекс Флеша в допустимом диапазоне."""
        analyzer = TextAnalyzer()
        text = "The cat sat on the mat. The dog ran fast. Birds fly in the sky."
        result = analyzer.analyze(text)
        assert 0 <= result.flesch_score <= 100
    
    def test_difficulty_level_set(self):
        """Уровень сложности установлен."""
        analyzer = TextAnalyzer()
        text = "Simple words here. Short sentences work. Easy to read this text."
        result = analyzer.analyze(text)
        assert result.difficulty_level != ""
    
    def test_recommendations_exist(self):
        """Рекомендации существуют."""
        analyzer = TextAnalyzer()
        text = "This is a test. We write simple text. It should be easy to read now."
        result = analyzer.analyze(text)
        assert len(result.recommendations) > 0


class TestTextAnalyzerRussian:
    """Тесты для русского языка."""
    
    def test_russian_text(self):
        """Анализ русского текста."""
        analyzer = TextAnalyzer(language="ru")
        text = "Это простой текст. Он на русском языке. Здесь несколько предложений для теста."
        result = analyzer.analyze(text)
        assert result.word_count > 0


class TestReadabilityResult:
    """Тесты ReadabilityResult."""
    
    def test_to_dict(self):
        """Преобразование в словарь."""
        result = ReadabilityResult(
            text_length=100,
            word_count=20,
            sentence_count=4,
            avg_word_length=4.5,
            avg_sentence_length=5.0,
            flesch_score=75.0,
            flesch_kincaid=5.0,
            coleman_liau=6.0,
            ari=5.5,
            difficulty_level="Легко",
            target_audience="Средняя школа",
            recommendations=["OK"]
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d['word_count'] == 20
    
    def test_to_markdown(self):
        """Преобразование в Markdown."""
        result = ReadabilityResult(
            text_length=100,
            word_count=20,
            sentence_count=4,
            avg_word_length=4.5,
            avg_sentence_length=5.0,
            flesch_score=75.0,
            flesch_kincaid=5.0,
            coleman_liau=6.0,
            ari=5.5,
            difficulty_level="Легко",
            target_audience="Средняя школа",
            recommendations=["OK"]
        )
        md = result.to_markdown()
        assert isinstance(md, str)
        assert "20" in md