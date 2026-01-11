"""
Тесты для главного класса TextAnalyzer.
"""

import pytest
from src.analyzer import TextAnalyzer, ReadabilityResult


class TestTextAnalyzerInit:
    """Тесты инициализации анализатора."""
    
    def test_default_language(self):
        """По умолчанию язык 'auto'."""
        analyzer = TextAnalyzer()
        assert analyzer.language == "auto"
    
    def test_english_language(self):
        """Установка английского языка."""
        analyzer = TextAnalyzer(language="en")
        assert analyzer.language == "en"
    
    def test_russian_language(self):
        """Установка русского языка."""
        analyzer = TextAnalyzer(language="ru")
        assert analyzer.language == "ru"


class TestTextAnalyzerAnalyze:
    """Тесты метода analyze."""
    
    @pytest.fixture
    def analyzer(self):
        """Фикстура анализатора."""
        return TextAnalyzer(language="en")
    
    @pytest.fixture
    def simple_text(self):
        """Простой текст для тестов."""
        return (
            "The cat sat on the mat. "
            "The dog ran in the park. "
            "Birds fly high in the sky. "
            "Fish swim in the sea."
        )
    
    @pytest.fixture
    def complex_text(self):
        """Сложный текст для тестов."""
        return (
            "The implementation of sophisticated algorithmic paradigms "
            "necessitates comprehensive understanding of computational "
            "complexity theory and mathematical abstractions that underpin "
            "modern software engineering methodologies utilized in "
            "enterprise-level application development and deployment."
        )
    
    def test_returns_readability_result(self, analyzer, simple_text):
        """Метод возвращает ReadabilityResult."""
        result = analyzer.analyze(simple_text)
        assert isinstance(result, ReadabilityResult)
    
    def test_empty_text_raises_error(self, analyzer):
        """Пустой текст вызывает ошибку."""
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("")
        assert "пустым" in str(exc_info.value).lower()
    
    def test_whitespace_only_raises_error(self, analyzer):
        """Текст из пробелов вызывает ошибку."""
        with pytest.raises(ValueError):
            analyzer.analyze("   \n\t  ")
    
    def test_short_text_raises_error(self, analyzer):
        """Слишком короткий текст вызывает ошибку."""
        with pytest.raises(ValueError) as exc_info:
            analyzer.analyze("Hello world.")
        assert "короткий" in str(exc_info.value).lower()
    
    def test_word_count_correct(self, analyzer, simple_text):
        """Правильный подсчёт слов."""
        result = analyzer.analyze(simple_text)
        assert result.word_count > 0
        # В нашем тексте около 20 слов
        assert 15 <= result.word_count <= 25
    
    def test_sentence_count_correct(self, analyzer, simple_text):
        """Правильный подсчёт предложений."""
        result = analyzer.analyze(simple_text)
        assert result.sentence_count == 4
    
    def test_simple_text_easy_score(self, analyzer, simple_text):
        """Простой текст имеет высокий индекс Флеша."""
        result = analyzer.analyze(simple_text)
        assert result.flesch_score >= 70, f"Expected >= 70, got {result.flesch_score}"
    
    def test_complex_text_hard_score(self, analyzer, complex_text):
        """Сложный текст имеет низкий индекс Флеша."""
        result = analyzer.analyze(complex_text)
        assert result.flesch_score < 50, f"Expected < 50, got {result.flesch_score}"
    
    def test_difficulty_level_set(self, analyzer, simple_text):
        """Уровень сложности определён."""
        result = analyzer.analyze(simple_text)
        assert result.difficulty_level != ""
        assert result.difficulty_level != "Неопределённо"
    
    def test_target_audience_set(self, analyzer, simple_text):
        """Целевая аудитория определена."""
        result = analyzer.analyze(simple_text)
        assert result.target_audience != ""
        assert result.target_audience != "Неизвестно"
    
    def test_recommendations_generated(self, analyzer, complex_text):
        """Рекомендации генерируются."""
        result = analyzer.analyze(complex_text)
        assert len(result.recommendations) > 0
    
    def test_avg_word_length_reasonable(self, analyzer, simple_text):
        """Средняя длина слова в разумных пределах."""
        result = analyzer.analyze(simple_text)
        assert 2 <= result.avg_word_length <= 15
    
    def test_avg_sentence_length_reasonable(self, analyzer, simple_text):
        """Средняя длина предложения в разумных пределах."""
        result = analyzer.analyze(simple_text)
        assert 3 <= result.avg_sentence_length <= 50


class TestTextAnalyzerRussian:
    """Тесты для русского языка."""
    
    @pytest.fixture
    def analyzer(self):
        """Фикстура анализатора для русского."""
        return TextAnalyzer(language="ru")
    
    @pytest.fixture
    def russian_text(self):
        """Текст на русском языке."""
        return (
            "Это простой текст на русском языке. "
            "Он содержит несколько коротких предложений. "
            "Каждое предложение легко читать. "
            "Слова в нём простые и понятные."
        )
    
    def test_russian_text_analyzed(self, analyzer, russian_text):
        """Русский текст анализируется."""
        result = analyzer.analyze(russian_text)
        assert isinstance(result, ReadabilityResult)
    
    def test_russian_word_count(self, analyzer, russian_text):
        """Слова на русском считаются."""
        result = analyzer.analyze(russian_text)
        assert result.word_count > 15


class TestTextAnalyzerAutoLanguage:
    """Тесты автоопределения языка."""
    
    def test_auto_detects_english(self):
        """Автоопределение английского."""
        analyzer = TextAnalyzer(language="auto")
        text = "This is a simple English text with several sentences for testing purposes."
        result = analyzer.analyze(text)
        assert result.word_count > 0
    
    def test_auto_detects_russian(self):
        """Автоопределение русского."""
        analyzer = TextAnalyzer(language="auto")
        text = "Это простой текст на русском языке для тестирования автоопределения языка системой."
        result = analyzer.analyze(text)
        assert result.word_count > 0


class TestReadabilityResult:
    """Тесты класса ReadabilityResult."""
    
    @pytest.fixture
    def sample_result(self):
        """Пример результата."""
        return ReadabilityResult(
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
            recommendations=["Текст хорошо сбалансирован"]
        )
    
    def test_to_dict(self, sample_result):
        """Преобразование в словарь."""
        d = sample_result.to_dict()
        assert isinstance(d, dict)
        assert 'word_count' in d
        assert d['word_count'] == 20
    
    def test_to_markdown(self, sample_result):
        """Преобразование в Markdown."""
        md = sample_result.to_markdown()
        assert isinstance(md, str)
        assert "##" in md  # Заголовки Markdown
        assert "20" in md  # word_count
    
    def test_str_representation(self, sample_result):
        """Строковое представление."""
        s = str(sample_result)
        assert "ReadabilityResult" in s
        assert "20" in s  # word_count