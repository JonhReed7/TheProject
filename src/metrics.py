"""
Модуль с формулами расчёта читабельности текста.
"""
import re
from typing import Dict


def count_syllables(word: str) -> int:
    """Подсчёт слогов в слове (для английского)."""
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    
    # Корректировка для немых 'e'
    if word.endswith('e') and count > 1:
        count -= 1
    
    return max(1, count)


def count_syllables_ru(word: str) -> int:
    """Подсчёт слогов в русском слове."""
    vowels = "аеёиоуыэюя"
    return max(1, sum(1 for char in word.lower() if char in vowels))


def flesch_reading_ease(total_words: int, 
                         total_sentences: int, 
                         total_syllables: int) -> float:
    """
    Индекс удобочитаемости Флеша.
    
    Шкала:
    - 90-100: Очень легко (5 класс)
    - 60-70: Стандартный текст
    - 0-30: Очень сложно (университет)
    """
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return round(max(0, min(100, score)), 2)


def coleman_liau_index(total_chars: int, 
                        total_words: int, 
                        total_sentences: int) -> float:
    """
    Индекс Коулмана-Лиау.
    Возвращает примерный уровень класса (US grade level).
    """
    if total_words == 0:
        return 0.0
    
    L = (total_chars / total_words) * 100  # Среднее кол-во букв на 100 слов
    S = (total_sentences / total_words) * 100  # Среднее кол-во предложений на 100 слов
    
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(max(0, index), 2)


def automated_readability_index(total_chars: int, 
                                  total_words: int, 
                                  total_sentences: int) -> float:
    """
    Автоматический индекс читабельности (ARI).
    Возвращает уровень класса.
    """
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_word_length = total_chars / total_words
    avg_sentence_length = total_words / total_sentences
    
    ari = 4.71 * avg_word_length + 0.5 * avg_sentence_length - 21.43
    return round(max(0, ari), 2)