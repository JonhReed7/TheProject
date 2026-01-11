"""Тесты для главного анализатора."""
import pytest
from src.analyzer import TextAnalyzer, ReadabilityResult


class TestTextAnalyzer:
    """Тесты класса TextAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return TextAnalyzer(language="en")
    
    @pytest.fixture
    def simple_text(self):
        return "The cat sat on the mat. The dog ran fast. Birds fly high in the sky."
    
    @pytest.fixture
    def complex_text(self):
        return """
        The implementation of sophisticated algorithmic paradigms necessitates 
        comprehensive understanding of computational complexity theory and 
        mathematical abstractions that underpin modern software engineering 
        methodologies utilized in enterprise-level application development.
        """
    
    def test_analyze_returns_result(self, analyzer, simple_text):
        result = analyzer.analyze(simple_text)
        assert isinstance(result, ReadabilityResult)
    
    def test_analyze_empty_text_raises(self, analyzer):
        with pytest.raises(ValueError, match="не может быть пустым"):
            analyzer.analyze("")
    
    def test_analyze_short_text_raises(self, analyzer):
        with pytest.raises(ValueError, match="слишком короткий"):
            analyzer.analyze("Hello world.")
    
    def test_simple_text_is_easy(self, analyzer, simple_text):
        result = analyzer.analyze(simple_text)
        assert result.flesch_score > 60
        assert "легко" in result.difficulty_level.lower() or result.flesch_score > 70
    
    def test_complex_text_is_hard(self, analyzer, complex_text):
        result = analyzer.analyze(complex_text)
        assert result.flesch_score < 50
    
    def test_word_count_correct(self, analyzer, simple_text):
        result = analyzer.analyze(simple_text)
        assert result.word_count > 0
        assert result.sentence_count == 3
    
    def test_recommendations_generated(self, analyzer, complex_text):
        result = analyzer.analyze(complex_text)
        assert len(result.recommendations) > 0
    
    def test_russian_language(self):
        analyzer_ru = TextAnalyzer(language="ru")
        text = "Это простой текст на русском языке. Он содержит несколько предложений. Каждое предложение короткое и понятное."
        result = analyzer_ru.analyze(text)
        assert result.word_count > 0