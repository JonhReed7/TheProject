"""
Главный модуль анализатора читабельности.
"""
import re
from dataclasses import dataclass
from typing import Optional

from .metrics import (
    flesch_reading_ease,
    coleman_liau_index,
    automated_readability_index,
    count_syllables,
    count_syllables_ru
)


@dataclass
class ReadabilityResult:
    """Результат анализа читабельности."""
    text_length: int
    word_count: int
    sentence_count: int
    avg_word_length: float
    avg_sentence_length: float
    flesch_score: float
    coleman_liau: float
    ari: float
    difficulty_level: str
    target_audience: str
    recommendations: list


class TextAnalyzer:
    """Анализатор читабельности текста."""
    
    DIFFICULTY_LEVELS = {
        (90, 100): ("Очень легко", "Начальная школа (1-4 класс)"),
        (70, 89): ("Легко", "Средняя школа (5-7 класс)"),
        (50, 69): ("Средне", "Старшая школа (8-11 класс)"),
        (30, 49): ("Сложно", "Студенты бакалавриата"),
        (0, 29): ("Очень сложно", "Магистратура / Специалисты"),
    }
    
    def __init__(self, language: str = "en"):
        """
        Инициализация анализатора.
        
        Args:
            language: Язык текста ('en' или 'ru')
        """
        self.language = language
        self._syllable_counter = count_syllables_ru if language == "ru" else count_syllables
    
    def _tokenize_sentences(self, text: str) -> list:
        """Разбивка текста на предложения."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _tokenize_words(self, text: str) -> list:
        """Разбивка текста на слова."""
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _count_characters(self, words: list) -> int:
        """Подсчёт букв (без пробелов и знаков)."""
        return sum(len(word) for word in words)
    
    def _count_total_syllables(self, words: list) -> int:
        """Подсчёт общего количества слогов."""
        return sum(self._syllable_counter(word) for word in words)
    
    def _get_difficulty_level(self, flesch_score: float) -> tuple:
        """Определение уровня сложности по индексу Флеша."""
        for (low, high), (level, audience) in self.DIFFICULTY_LEVELS.items():
            if low <= flesch_score <= high:
                return level, audience
        return "Неопределённо", "Неизвестно"
    
    def _generate_recommendations(self, result: dict) -> list:
        """Генерация рекомендаций по улучшению текста."""
        recommendations = []
        
        if result["avg_sentence_length"] > 25:
            recommendations.append(
                "📝 Сократите предложения: средняя длина > 25 слов. "
                "Разбейте длинные предложения на короткие."
            )
        
        if result["avg_word_length"] > 6:
            recommendations.append(
                "📖 Используйте более простые слова: средняя длина > 6 букв. "
                "Замените сложные термины на простые синонимы."
            )
        
        if result["flesch_score"] < 30:
            recommendations.append(
                "⚠️ Текст очень сложный для восприятия. "
                "Добавьте пояснения и примеры."
            )
        
        if not recommendations:
            recommendations.append("✅ Текст хорошо сбалансирован!")
        
        return recommendations
    
    def analyze(self, text: str) -> ReadabilityResult:
        """
        Анализ читабельности текста.
        
        Args:
            text: Текст для анализа
            
        Returns:
            ReadabilityResult с метриками и рекомендациями
        """
        if not text or not text.strip():
            raise ValueError("Текст не может быть пустым")
        
        sentences = self._tokenize_sentences(text)
        words = self._tokenize_words(text)
        
        if len(words) < 10:
            raise ValueError("Текст слишком короткий (минимум 10 слов)")
        
        total_chars = self._count_characters(words)
        total_syllables = self._count_total_syllables(words)
        
        word_count = len(words)
        sentence_count = max(1, len(sentences))
        
        avg_word_length = round(total_chars / word_count, 2)
        avg_sentence_length = round(word_count / sentence_count, 2)
        
        flesch = flesch_reading_ease(word_count, sentence_count, total_syllables)
        coleman = coleman_liau_index(total_chars, word_count, sentence_count)
        ari = automated_readability_index(total_chars, word_count, sentence_count)
        
        difficulty, audience = self._get_difficulty_level(flesch)
        
        intermediate = {
            "avg_sentence_length": avg_sentence_length,
            "avg_word_length": avg_word_length,
            "flesch_score": flesch,
        }
        recommendations = self._generate_recommendations(intermediate)
        
        return ReadabilityResult(
            text_length=len(text),
            word_count=word_count,
            sentence_count=sentence_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            flesch_score=flesch,
            coleman_liau=coleman,
            ari=ari,
            difficulty_level=difficulty,
            target_audience=audience,
            recommendations=recommendations
        )
    
    def analyze_file(self, filepath: str) -> ReadabilityResult:
        """Анализ текста из файла."""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.analyze(text)