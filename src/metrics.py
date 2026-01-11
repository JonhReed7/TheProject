"""Модуль с формулами расчёта читабельности текста."""


def count_syllables(word):
    """Подсчёт слогов в английском слове."""
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
    
    if word.endswith('e') and count > 1:
        count -= 1
    
    return max(1, count)


def count_syllables_ru(word):
    """Подсчёт слогов в русском слове."""
    word = word.lower().strip()
    if not word:
        return 0
    
    vowels = "аеёиоуыэюя"
    count = sum(1 for char in word if char in vowels)
    
    return max(1, count)


def flesch_reading_ease(total_words, total_sentences, total_syllables):
    """Индекс удобочитаемости Флеша (0-100)."""
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    return round(max(0, min(100, score)), 2)


def flesch_kincaid_grade(total_words, total_sentences, total_syllables):
    """Уровень класса по Флешу-Кинкейду."""
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    
    return round(max(0, grade), 2)


def coleman_liau_index(total_chars, total_words, total_sentences):
    """Индекс Коулмана-Лиау."""
    if total_words == 0:
        return 0.0
    
    L = (total_chars / total_words) * 100
    S = (total_sentences / total_words) * 100
    
    index = 0.0588 * L - 0.296 * S - 15.8
    
    return round(max(0, index), 2)


def automated_readability_index(total_chars, total_words, total_sentences):
    """Автоматический индекс читабельности (ARI)."""
    if total_words == 0 or total_sentences == 0:
        return 0.0
    
    avg_chars_per_word = total_chars / total_words
    avg_words_per_sentence = total_words / total_sentences
    
    ari = 4.71 * avg_chars_per_word + 0.5 * avg_words_per_sentence - 21.43
    
    return round(max(0, ari), 2)