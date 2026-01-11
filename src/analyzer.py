"""Главный модуль анализатора читабельности."""

import re
from dataclasses import dataclass, field
from typing import List

from .metrics import (
    flesch_reading_ease,
    flesch_kincaid_grade,
    coleman_liau_index,
    automated_readability_index,
    count_syllables,
    count_syllables_ru
)
from .utils import (
    tokenize_sentences,
    tokenize_words,
    count_characters,
    clean_text,
    detect_language
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
    flesch_kincaid: float
    coleman_liau: float
    ari: float
    difficulty_level: str
    target_audience: str
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self):
        """Преобразование в словарь."""
        return {
            'text_length': self.text_length,
            'word_count': self.word_count,
            'sentence_count': self.sentence_count,
            'avg_word_length': self.avg_word_length,
            'avg_sentence_length': self.avg_sentence_length,
            'flesch_score': self.flesch_score,
            'difficulty_level': self.difficulty_level,
            'target_audience': self.target_audience,
        }
    
    def to_markdown(self, title="Analysis"):
        """Преобразование в Markdown."""
        lines = [
            f"## {title}",
            f"- Words: {self.word_count}",
            f"- Flesch Score: {self.flesch_score}",
            f"- Difficulty: {self.difficulty_level}",
        ]
        return "\n".join(lines)


class TextAnalyzer:
    """Анализатор читабельности текста."""
    
    DIFFICULTY_THRESHOLDS = {
        (90, 100): ("Очень легко", "Начальная школа (1-4 класс)"),
        (70, 89): ("Легко", "Средняя школа (5-7 класс)"),
        (50, 69): ("Средне", "Старшая школа (8-11 класс)"),
        (30, 49): ("Сложно", "Студенты бакалавриата"),
        (0, 29): ("Очень сложно", "Магистратура / Специалисты"),
    }
    
    MIN_WORDS = 10
    
    def __init__(self, language="auto"):
        """Инициализация анализатора."""
        self.language = language
        self._syllable_func = None
        
        if language == 'ru':
            self._syllable_func = count_syllables_ru
        elif language == 'en':
            self._syllable_func = count_syllables
    
    def _get_syllable_counter(self, text):
        """Получение функции подсчёта слогов."""
        if self._syllable_func:
            return self._syllable_func
        
        detected_lang = detect_language(text)
        return count_syllables_ru if detected_lang == 'ru' else count_syllables
    
    def _get_difficulty_level(self, flesch_score):
        """Определение уровня сложности."""
        for (low, high), (level, audience) in self.DIFFICULTY_THRESHOLDS.items():
            if low <= flesch_score <= high:
                return level, audience
        return "Неопределённо", "Неизвестно"
    
    def _generate_recommendations(self, avg_sentence_length, avg_word_length, flesch_score):
        """Генерация рекомендаций."""
        recommendations = []
        
        if avg_sentence_length > 25:
            recommendations.append("Сократите предложения (средняя длина > 25 слов).")
        
        if avg_word_length > 7:
            recommendations.append("Используйте более простые слова.")
        
        if flesch_score < 30:
            recommendations.append("Текст очень сложный, добавьте пояснения.")
        
        if not recommendations:
            recommendations.append("Текст хорошо сбалансирован!")
        
        return recommendations
    
    def analyze(self, text):
        """Анализ читабельности текста."""
        if not text or not text.strip():
            raise ValueError("Текст не может быть пустым")
        
        text = clean_text(text)
        sentences = tokenize_sentences(text)
        words = tokenize_words(text)
        
        if len(words) < self.MIN_WORDS:
            raise ValueError(f"Текст слишком короткий (минимум {self.MIN_WORDS} слов)")
        
        syllable_counter = self._get_syllable_counter(text)
        
        total_chars = count_characters(words)
        total_syllables = sum(syllable_counter(word) for word in words)
        
        word_count = len(words)
        sentence_count = max(1, len(sentences))
        
        avg_word_length = round(total_chars / word_count, 2)
        avg_sentence_length = round(word_count / sentence_count, 2)
        
        flesch = flesch_reading_ease(word_count, sentence_count, total_syllables)
        fk_grade = flesch_kincaid_grade(word_count, sentence_count, total_syllables)
        coleman = coleman_liau_index(total_chars, word_count, sentence_count)
        ari = automated_readability_index(total_chars, word_count, sentence_count)
        
        difficulty, audience = self._get_difficulty_level(flesch)
        recommendations = self._generate_recommendations(avg_sentence_length, avg_word_length, flesch)
        
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
    
    def analyze_file(self, filepath):
        """Анализ текста из файла."""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.analyze(text)