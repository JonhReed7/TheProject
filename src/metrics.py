"""
Модуль с формулами расчёта читабельности текста.

Содержит реализации популярных индексов:
- Flesch Reading Ease
- Coleman-Liau Index
- Automated Readability Index (ARI)
- Flesch-Kincaid Grade Level
"""

import re
from typing import List, Tuple


def count_syllables(word: str) -> int:
    """
    Подсчёт количества слогов в английском слове.
    
    Алгоритм основан на подсчёте гласных с учётом:
    - Дифтонгов (две гласные подряд = один слог)
    - Немой 'e' в конце слова
    
    Args:
        word: Слово для анализа
        
    Returns:
        Количество слогов (минимум 1)
        
    Examples:
        >>> count_syllables("hello")
        2
        >>> count_syllables("world")
        1
        >>> count_syllables("beautiful")
        3
    """
    word = word.lower().strip()
    if not word:
        return 0
    
    vowels = "aeiouy"
    count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    
    # Корректировка для немой 'e' в конце
    if word.endswith('e') and count > 1:
        count -= 1
    
    # Корректировка для 'le' в конце (например, "table")
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    
    return max(1, count)


def count_syllables_ru(word: str) -> int:
    """
    Подсчёт количества слогов в русском слове.
    
    В русском языке количество слогов равно количеству гласных.
    
    Args:
        word: Слово для анализа
        
    Returns:
        Количество слогов (минимум 1)
        
    Examples:
        >>> count_syllables_ru("привет")
        2
        >>> count_syllables_ru("образование")
        6
    """
    word = word.lower().strip()
    if not word:
        return 0
    
    vowels = "аеёиоуыэюя"
    count = sum(1 for char in word if char in vowels)
    
    return max(1, count)


def flesch_reading_ease(total_words: int,
                        total_sentences: int,
                        total_syllables: int) -> float:
    """
    Расчёт индекса удобочитаемости Флеша (Flesch Reading Ease).
    
    Формула:
        206.835 - 1.015 × (words/sentences) - 84.6 × (syllables/words)
    
    Интерпретация шкалы:
        - 90-100: Очень легко читать (5 класс)
        - 80-89:  Легко читать (6 класс)
        - 70-79:  Довольно легко (7 класс)
        - 60-69:  Стандартный текст (8-9 класс)
        - 50-59:  Довольно сложно (10-12 класс)
        - 30-49:  Сложно (университет)
        - 0-29:   Очень сложно (специалисты)
    
    Args:
        total_words: Общее количество слов
        total_sentences: Общее количество предложений
        total_syllables: Общее количество слогов
        
    Returns:
        Индекс от 0 до 100 (может выходить за пределы)
    """
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    # Ограничиваем диапазон 0-100
    return round(max(0, min(100, score)), 2)


def flesch_kincaid_grade(total_words: int,
                         total_sentences: int,
                         total_syllables: int) -> float:
    """
    Расчёт уровня класса по Флешу-Кинкейду.
    
    Формула:
        0.39 × (words/sentences) + 11.8 × (syllables/words) - 15.59
    
    Результат соответствует уровню класса в американской системе.
    
    Args:
        total_words: Общее количество слов
        total_sentences: Общее количество предложений
        total_syllables: Общее количество слогов
        
    Returns:
        Уровень класса (например, 8.5 = 8-9 класс)
    """
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    
    return round(max(0, grade), 2)


def coleman_liau_index(total_chars: int,
                       total_words: int,
                       total_sentences: int) -> float:
    """
    Расчёт индекса Коулмана-Лиау.
    
    Особенность: использует количество букв вместо слогов,
    что делает его более точным для компьютерного анализа.
    
    Формула:
        0.0588 × L - 0.296 × S - 15.8
        где L = среднее кол-во букв на 100 слов
            S = среднее кол-во предложений на 100 слов
    
    Args:
        total_chars: Общее количество букв (без пробелов)
        total_words: Общее количество слов
        total_sentences: Общее количество предложений
        
    Returns:
        Уровень класса (US grade level)
    """
    if total_words == 0:
        return 0.0
    
    # L = среднее количество букв на 100 слов
    L = (total_chars / total_words) * 100
    
    # S = среднее количество предложений на 100 слов
    S = (total_sentences / total_words) * 100
    
    index = 0.0588 * L - 0.296 * S - 15.8
    
    return round(max(0, index), 2)


def automated_readability_index(total_chars: int,
                                total_words: int,
                                total_sentences: int) -> float:
    """
    Расчёт автоматического индекса читабельности (ARI).
    
    Формула:
        4.71 × (chars/words) + 0.5 × (words/sentences) - 21.43
    
    Преимущество: не требует подсчёта слогов.
    
    Args:
        total_chars: Общее количество букв
        total_words: Общее количество слов
        total_sentences: Общее количество предложений
        
    Returns:
        Уровень класса (US grade level)
    """
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_chars_per_word = total_chars / total_words
    avg_words_per_sentence = total_words / total_sentences
    
    ari = 4.71 * avg_chars_per_word + 0.5 * avg_words_per_sentence - 21.43
    
    return round(max(0, ari), 2)


def smog_index(total_polysyllables: int, total_sentences: int) -> float:
    """
    Расчёт индекса SMOG (Simple Measure of Gobbledygook).
    
    Формула:
        1.0430 × sqrt(polysyllables × (30/sentences)) + 3.1291
    
    Polysyllables = слова с 3+ слогами
    
    Args:
        total_polysyllables: Количество слов с 3+ слогами
        total_sentences: Общее количество предложений
        
    Returns:
        Уровень класса
    """
    if total_sentences == 0:
        return 0.0
    
    import math
    
    smog = 1.0430 * math.sqrt(total_polysyllables * (30 / total_sentences)) + 3.1291
    
    return round(max(0, smog), 2)


def get_grade_description(grade_level: float) -> Tuple[str, str]:
    """
    Получение описания уровня сложности по классу.
    
    Args:
        grade_level: Уровень класса (1-20)
        
    Returns:
        Кортеж (уровень сложности, целевая аудитория)
    """
    if grade_level <= 4:
        return ("Очень легко", "Начальная школа (1-4 класс)")
    elif grade_level <= 6:
        return ("Легко", "Средняя школа (5-6 класс)")
    elif grade_level <= 8:
        return ("Средне", "Средняя школа (7-8 класс)")
    elif grade_level <= 10:
        return ("Умеренно сложно", "Старшая школа (9-10 класс)")
    elif grade_level <= 12:
        return ("Сложно", "Старшая школа (11-12 класс)")
    elif grade_level <= 16:
        return ("Очень сложно", "Бакалавриат")
    else:
        return ("Академический", "Магистратура / Специалисты")