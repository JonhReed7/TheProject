"""Вспомогательные утилиты."""

import re


def tokenize_sentences(text):
    """Разбивка текста на предложения."""
    if not text:
        return []
    
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def tokenize_words(text):
    """Разбивка текста на слова."""
    if not text:
        return []
    
    words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', text.lower())
    return words


def count_characters(words):
    """Подсчёт общего количества символов."""
    return sum(len(word) for word in words)


def clean_text(text):
    """Очистка текста."""
    if not text:
        return ""
    
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_language(text):
    """Определение языка текста."""
    if not text:
        return 'en'
    
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    return 'ru' if russian_chars > english_chars else 'en'