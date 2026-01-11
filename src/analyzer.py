"""
Главный модуль анализатора читабельности текста.

Содержит класс TextAnalyzer для комплексного анализа
читабельности учебных материалов.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from .metrics import (
    flesch_reading_ease,
    flesch_kincaid_grade,
    coleman_liau_index,
    automated_readability_index,
    smog_index,
    count_syllables,
    count_syllables_ru,
    get_grade_description
)
from .utils import (
    tokenize_sentences,
    tokenize_words,
    count_characters,
    clean_text,
    detect_language,
    read_text_file,
    format_result_as_markdown,
    format_result_as_dict
)


@dataclass
class ReadabilityResult:
    """
    Результат анализа читабельности текста.
    
    Attributes:
        text_length: Длина текста в символах
        word_count: Количество слов
        sentence_count: Количество предложений
        avg_word_length: Средняя длина слова в буквах
        avg_sentence_length: Средняя длина предложения в словах
        flesch_score: Индекс удобочитаемости Флеша (0-100)
        flesch_kincaid: Уровень класса по Флешу-Кинкейду
        coleman_liau: Индекс Коулмана-Лиау
        ari: Автоматический индекс читабельности
        difficulty_level: Уровень сложности (текстовое описание)
        target_audience: Целевая аудитория
        recommendations: Список рекомендаций по улучшению
    """
    text_length: int
    word_count: int
    sentence_count: int
    avg_word_length: float
    avg_sentence_length: float
    flesch_score: float
    flesch_kincaid: float
    coleman_liau: float
    ari: float
    difficulty_level: str
    target_audience: str
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь."""
        return format_result_as_dict(self)
    
    def to_markdown(self, title: str = "Analysis Result") -> str:
        """Преобразование в Markdown."""
        return format_result_as_markdown(self, title)
    
    def __str__(self) -> str:
        """Строковое представление результата."""
        return (
            f"ReadabilityResult(\n"
            f"  words={self.word_count}, "
            f"sentences={self.sentence_count},\n"
            f"  flesch={self.flesch_score}, "
            f"difficulty='{self.difficulty_level}',\n"
            f"  audience='{self.target_audience}'\n"
            f")"
        )


class TextAnalyzer:
    """
    Анализатор читабельности текста.
    
    Вычисляет различные метрики читабельности и определяет
    целевую аудиторию для учебных материалов.
    
    Attributes:
        language: Язык анализируемого текста ('en' или 'ru')
        
    Examples:
        >>> analyzer = TextAnalyzer(language='en')
        >>> result = analyzer.analyze("The cat sat on the mat.")
        >>> print(result.difficulty_level)
        'Очень легко'
    """
    
    # Пороги для определения сложности по индексу Флеша
    DIFFICULTY_THRESHOLDS = {
        (90, 100): ("Очень легко", "Начальная школа (1-4 класс)"),
        (70, 89): ("Легко", "Средняя школа (5-7 класс)"),
        (50, 69): ("Средне", "Старшая школа (8-11 класс)"),
        (30, 49): ("Сложно", "Студенты бакалавриата"),
        (0, 29): ("Очень сложно", "Магистратура / Специалисты"),
    }
    
    # Минимальные требования к тексту
    MIN_WORDS = 10
    MIN_SENTENCES = 1
    
    def __init__(self, language: str = "auto"):
        """
        Инициализация анализатора.
        
        Args:
            language: Язык текста ('en', 'ru' или 'auto' для автоопределения)
        """
        self.language = language
        self._syllable_func = None
        
        if language == 'ru':
            self._syllable_func = count_syllables_ru
        elif language == 'en':
            self._syllable_func = count_syllables
        # При 'auto' функция выбирается при анализе
    
    def _get_syllable_counter(self, text: str):
        """Получение функции подсчёта слогов."""
        if self._syllable_func:
            return self._syllable_func
        
        # Автоопределение языка
        detected_lang = detect_language(text)
        return count_syllables_ru if detected_lang == 'ru' else count_syllables
    
    def _count_total_syllables(self, words: List[str], syllable_func) -> int:
        """Подсчёт общего количества слогов."""
        return sum(syllable_func(word) for word in words)
    
    def _count_polysyllables(self, words: List[str], syllable_func) -> int:
        """Подсчёт слов с 3+ слогами."""
        return sum(1 for word in words if syllable_func(word) >= 3)
    
    def _get_difficulty_level(self, flesch_score: float) -> tuple:
        """
        Определение уровня сложности по индексу Флеша.
        
        Args:
            flesch_score: Индекс Флеша (0-100)
            
        Returns:
            Кортеж (уровень сложности, целевая аудитория)
        """
        for (low, high), (level, audience) in self.DIFFICULTY_THRESHOLDS.items():
            if low <= flesch_score <= high:
                return level, audience
        return "Неопределённо", "Неизвестно"
    
    def _generate_recommendations(self, 
                                   avg_sentence_length: float,
                                   avg_word_length: float,
                                   flesch_score: float,
                                   word_count: int) -> List[str]:
        """
        Генерация рекомендаций по улучшению читабельности.
        
        Args:
            avg_sentence_length: Средняя длина предложения
            avg_word_length: Средняя длина слова
            flesch_score: Индекс Флеша
            word_count: Количество слов
            
        Returns:
            Список рекомендаций
        """
        recommendations = []
        
        # Проверка длины предложений
        if avg_sentence_length > 25:
            recommendations.append(
                "📝 **Сократите предложения:** средняя длина составляет "
                f"{avg_sentence_length:.1f} слов (рекомендуется до 20-25). "
                "Разбейте длинные предложения на более короткие."
            )
        elif avg_sentence_length > 20:
            recommendations.append(
                "📝 Предложения немного длинноваты. "
                "Рассмотрите возможность их упрощения."
            )
        
        # Проверка длины слов
        if avg_word_length > 7:
            recommendations.append(
                "📖 **Упростите лексику:** средняя длина слова "
                f"{avg_word_length:.1f} букв (рекомендуется до 5-6). "
                "Замените сложные термины на более простые синонимы."
            )
        elif avg_word_length > 6:
            recommendations.append(
                "📖 Попробуйте использовать более короткие и простые слова."
            )
        
        # Проверка общего индекса
        if flesch_score < 30:
            recommendations.append(
                "⚠️ **Текст очень сложный** для большинства читателей. "
                "Добавьте пояснения, примеры и разбейте сложные концепции "
                "на более простые части."
            )
        elif flesch_score < 50:
            recommendations.append(
                "💡 Текст подходит для подготовленной аудитории. "
                "Для более широкого круга читателей рекомендуется упростить."
            )
        
        # Проверка объёма текста
        if word_count < 100:
            recommendations.append(
                "📄 Текст довольно короткий. Результаты анализа могут быть "
                "менее точными для коротких текстов."
            )
        
        # Если нет проблем
        if not recommendations:
            recommendations.append(
                "✅ **Отличная читабельность!** Текст хорошо сбалансирован "
                "и подходит для широкой аудитории."
            )
        
        return recommendations
    
    def analyze(self, text: str) -> ReadabilityResult:
        """
        Выполнение полного анализа читабельности текста.
        
        Args:
            text: Текст для анализа
            
        Returns:
            ReadabilityResult с метриками и рекомендациями
            
        Raises:
            ValueError: Если текст пустой или слишком короткий
            
        Examples:
            >>> analyzer = TextAnalyzer()
            >>> result = analyzer.analyze("This is a simple test. It has short sentences.")
            >>> print(result.flesch_score)
            82.5
        """
        # Валидация входных данных
        if not text or not text.strip():
            raise ValueError("Текст не может быть пустым")
        
        # Очистка текста
        text = clean_text(text)
        
        # Токенизация
        sentences = tokenize_sentences(text)
        words = tokenize_words(text)
        
        # Проверка минимальных требований
        if len(words) < self.MIN_WORDS:
            raise ValueError(
                f"Текст слишком короткий: {len(words)} слов "
                f"(минимум {self.MIN_WORDS})"
            )
        
        if len(sentences) < self.MIN_SENTENCES:
            raise ValueError(
                f"В тексте должно быть минимум {self.MIN_SENTENCES} предложение"
            )
        
        # Получаем функцию подсчёта слогов
        syllable_counter = self._get_syllable_counter(text)
        
        # Базовые подсчёты
        total_chars = count_characters(words)
        total_syllables = self._count_total_syllables(words, syllable_counter)
        total_polysyllables = self._count_polysyllables(words, syllable_counter)
        
        word_count = len(words)
        sentence_count = len(sentences)
        
        # Средние значения
        avg_word_length = round(total_chars / word_count, 2)
        avg_sentence_length = round(word_count / sentence_count, 2)
        
        # Расчёт индексов
        flesch = flesch_reading_ease(word_count, sentence_count, total_syllables)
        fk_grade = flesch_kincaid_grade(word_count, sentence_count, total_syllables)
        coleman = coleman_liau_index(total_chars, word_count, sentence_count)
        ari = automated_readability_index(total_chars, word_count, sentence_count)
        
        # Определение сложности
        difficulty, audience = self._get_difficulty_level(flesch)
        
        # Генерация рекомендаций
        recommendations = self._generate_recommendations(
            avg_sentence_length, 
            avg_word_length, 
            flesch,
            word_count
        )
        
        return ReadabilityResult(
            text_length=len(text),
            word_count=word_count,
            sentence_count=sentence_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            flesch_score=flesch,
            flesch_kincaid=fk_grade,
            coleman_liau=coleman,
            ari=ari,
            difficulty_level=difficulty,
            target_audience=audience,
            recommendations=recommendations
        )
    
    def analyze_file(self, filepath: str) -> ReadabilityResult:
        """
        Анализ текста из файла.
        
        Args:
            filepath: Путь к текстовому файлу
            
        Returns:
            ReadabilityResult с результатами анализа
            
        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если текст не соответствует требованиям
        """
        text = read_text_file(filepath)
        return self.analyze(text)
    
    def compare_texts(self, texts: List[str], 
                      names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Сравнение читабельности нескольких текстов.
        
        Args:
            texts: Список текстов для сравнения
            names: Названия текстов (опционально)
            
        Returns:
            Список словарей с результатами для каждого текста
        """
        if names is None:
            names = [f"Текст {i+1}" for i in range(len(texts))]
        
        results = []
        for name, text in zip(names, texts):
            try:
                result = self.analyze(text)
                results.append({
                    'name': name,
                    'success': True,
                    'result': result.to_dict()
                })
            except ValueError as e:
                results.append({
                    'name': name,
                    'success': False,
                    'error': str(e)
                })
        
        return results