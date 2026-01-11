"""
Вспомогательные утилиты для анализатора читабельности.

Содержит функции для:
- Токенизации текста
- Очистки текста
- Форматирования результатов
- Работы с файлами
"""

import re
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


def tokenize_sentences(text: str) -> List[str]:
    """
    Разбивка текста на предложения.
    
    Учитывает:
    - Точки, восклицательные и вопросительные знаки
    - Многоточие
    - Сокращения (Mr., Dr., etc.)
    
    Args:
        text: Исходный текст
        
    Returns:
        Список предложений
        
    Examples:
        >>> tokenize_sentences("Hello world. How are you?")
        ['Hello world', 'How are you']
    """
    if not text:
        return []
    
    # Защита сокращений
    abbreviations = ['Mr.', 'Mrs.', 'Dr.', 'Prof.', 'Jr.', 'Sr.', 
                     'vs.', 'etc.', 'e.g.', 'i.e.', 'т.д.', 'т.п.', 
                     'др.', 'пр.', 'г.', 'гг.']
    
    protected_text = text
    for abbr in abbreviations:
        protected_text = protected_text.replace(abbr, abbr.replace('.', '<DOT>'))
    
    # Разбиваем по концам предложений
    sentences = re.split(r'[.!?]+', protected_text)
    
    # Восстанавливаем точки и очищаем
    result = []
    for s in sentences:
        s = s.replace('<DOT>', '.').strip()
        if s:
            result.append(s)
    
    return result


def tokenize_words(text: str) -> List[str]:
    """
    Разбивка текста на слова.
    
    Извлекает только слова, игнорируя:
    - Знаки препинания
    - Числа (опционально)
    - Специальные символы
    
    Args:
        text: Исходный текст
        
    Returns:
        Список слов в нижнем регистре
        
    Examples:
        >>> tokenize_words("Hello, World! 123")
        ['hello', 'world']
    """
    if not text:
        return []
    
    # Извлекаем только буквенные последовательности
    words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', text.lower())
    
    return words


def count_characters(words: List[str]) -> int:
    """
    Подсчёт общего количества символов в словах.
    
    Args:
        words: Список слов
        
    Returns:
        Общее количество букв
    """
    return sum(len(word) for word in words)


def clean_text(text: str) -> str:
    """
    Очистка текста от лишних пробелов и спецсимволов.
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный текст
    """
    if not text:
        return ""
    
    # Удаляем множественные пробелы
    text = re.sub(r'\s+', ' ', text)
    
    # Удаляем пробелы в начале и конце
    text = text.strip()
    
    return text


def detect_language(text: str) -> str:
    """
    Определение языка текста (русский или английский).
    
    Args:
        text: Текст для анализа
        
    Returns:
        'ru' для русского, 'en' для английского
    """
    if not text:
        return 'en'
    
    # Подсчитываем русские и латинские буквы
    russian_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    return 'ru' if russian_chars > english_chars else 'en'


def format_result_as_dict(result: Any) -> Dict[str, Any]:
    """
    Форматирование результата анализа в словарь.
    
    Args:
        result: Объект ReadabilityResult
        
    Returns:
        Словарь с результатами
    """
    return {
        'text_length': result.text_length,
        'word_count': result.word_count,
        'sentence_count': result.sentence_count,
        'avg_word_length': result.avg_word_length,
        'avg_sentence_length': result.avg_sentence_length,
        'metrics': {
            'flesch_reading_ease': result.flesch_score,
            'coleman_liau_index': result.coleman_liau,
            'automated_readability_index': result.ari,
        },
        'difficulty_level': result.difficulty_level,
        'target_audience': result.target_audience,
        'recommendations': result.recommendations,
    }


def format_result_as_markdown(result: Any, title: str = "Analysis Result") -> str:
    """
    Форматирование результата анализа в Markdown.
    
    Args:
        result: Объект ReadabilityResult
        title: Заголовок отчёта
        
    Returns:
        Строка в формате Markdown
    """
    lines = [
        f"## 📊 {title}",
        "",
        "### Основные метрики",
        "",
        "| Метрика | Значение |",
        "|---------|----------|",
        f"| Длина текста | {result.text_length} символов |",
        f"| Количество слов | {result.word_count} |",
        f"| Количество предложений | {result.sentence_count} |",
        f"| Средняя длина слова | {result.avg_word_length} букв |",
        f"| Средняя длина предложения | {result.avg_sentence_length} слов |",
        "",
        "### Индексы читабельности",
        "",
        "| Индекс | Значение |",
        "|--------|----------|",
        f"| Flesch Reading Ease | {result.flesch_score} |",
        f"| Coleman-Liau Index | {result.coleman_liau} |",
        f"| ARI | {result.ari} |",
        "",
        "### Заключение",
        "",
        f"**Уровень сложности:** {result.difficulty_level}",
        "",
        f"**Целевая аудитория:** {result.target_audience}",
        "",
        "### Рекомендации",
        "",
    ]
    
    for rec in result.recommendations:
        lines.append(f"- {rec}")
    
    return "\n".join(lines)


def read_text_file(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Чтение текста из файла.
    
    Args:
        filepath: Путь к файлу
        encoding: Кодировка файла
        
    Returns:
        Содержимое файла
        
    Raises:
        FileNotFoundError: Если файл не найден
        IOError: При ошибке чтения
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def save_report(content: str, filepath: str, encoding: str = 'utf-8') -> None:
    """
    Сохранение отчёта в файл.
    
    Args:
        content: Содержимое отчёта
        filepath: Путь к файлу
        encoding: Кодировка файла
    """
    path = Path(filepath)
    
    # Создаём директорию, если не существует
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)


def get_text_statistics(text: str) -> Dict[str, int]:
    """
    Получение базовой статистики по тексту.
    
    Args:
        text: Исходный текст
        
    Returns:
        Словарь со статистикой
    """
    words = tokenize_words(text)
    sentences = tokenize_sentences(text)
    
    return {
        'characters_total': len(text),
        'characters_no_spaces': len(text.replace(' ', '')),
        'words': len(words),
        'sentences': len(sentences),
        'paragraphs': text.count('\n\n') + 1,
        'unique_words': len(set(words)),
    }