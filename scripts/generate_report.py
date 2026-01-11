#!/usr/bin/env python3
"""
Скрипт генерации отчёта по анализу читабельности текстов.

Использование:
    python scripts/generate_report.py --output reports/report.md --language en
    
Этот скрипт анализирует все тексты в data/sample_texts/ и генерирует
Markdown-отчёт с результатами.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Добавляем корневую директорию проекта в path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analyzer import TextAnalyzer


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Генерация отчёта по читабельности текстов"
    )
    parser.add_argument(
        '--output', '-o',
        default='reports/analysis_report.md',
        help='Путь к выходному файлу (default: reports/analysis_report.md)'
    )
    parser.add_argument(
        '--language', '-l',
        default='auto',
        choices=['en', 'ru', 'auto'],
        help='Язык текстов (default: auto)'
    )
    parser.add_argument(
        '--input-dir', '-i',
        default='data/sample_texts',
        help='Директория с текстами (default: data/sample_texts)'
    )
    return parser.parse_args()


def generate_report(analyzer: TextAnalyzer, 
                    input_dir: Path, 
                    language: str) -> str:
    """
    Генерация отчёта по всем текстам в директории.
    
    Args:
        analyzer: Экземпляр TextAnalyzer
        input_dir: Путь к директории с текстами
        language: Язык анализа
        
    Returns:
        Строка с отчётом в формате Markdown
    """
    lines = [
        "# 📊 Readability Analysis Report",
        "",
        f"**Дата генерации:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"**Язык анализа:** {language}",
        "",
        f"**Директория:** `{input_dir}`",
        "",
        "---",
        "",
        "## 📋 Сводная таблица",
        "",
        "| Файл | Слов | Предложений | Flesch | Сложность |",
        "|------|------|-------------|--------|-----------|",
    ]
    
    # Детальные результаты
    detailed_results = []
    
    # Анализируем все .txt файлы
    txt_files = sorted(input_dir.glob("*.txt"))
    
    if not txt_files:
        lines.append("| - | Нет файлов для анализа | - | - | - |")
    
    for txt_file in txt_files:
        try:
            result = analyzer.analyze_file(str(txt_file))
            
            # Строка для сводной таблицы
            lines.append(
                f"| {txt_file.name} | {result.word_count} | "
                f"{result.sentence_count} | {result.flesch_score} | "
                f"{result.difficulty_level} |"
            )
            
            # Детальный результат
            detailed_results.append((txt_file.name, result))
            
        except Exception as e:
            lines.append(f"| {txt_file.name} | ❌ Ошибка | - | - | {str(e)[:30]}... |")
    
    # Добавляем детальные результаты
    lines.extend([
        "",
        "---",
        "",
        "## 📄 Детальный анализ",
        "",
    ])
    
    for filename, result in detailed_results:
        lines.extend([
            f"### 📝 {filename}",
            "",
            "#### Основные метрики",
            "",
            "| Метрика | Значение |",
            "|---------|----------|",
            f"| Длина текста | {result.text_length} символов |",
            f"| Количество слов | {result.word_count} |",
            f"| Количество предложений | {result.sentence_count} |",
            f"| Средняя длина слова | {result.avg_word_length} букв |",
            f"| Средняя длина предложения | {result.avg_sentence_length} слов |",
            "",
            "#### Индексы читабельности",
            "",
            "| Индекс | Значение |",
            "|--------|----------|",
            f"| Flesch Reading Ease | {result.flesch_score} |",
            f"| Flesch-Kincaid Grade | {result.flesch_kincaid} |",
            f"| Coleman-Liau Index | {result.coleman_liau} |",
            f"| Automated Readability Index | {result.ari} |",
            "",
            "#### Заключение",
            "",
            f"- **Уровень сложности:** {result.difficulty_level}",
            f"- **Целевая аудитория:** {result.target_audience}",
            "",
            "#### Рекомендации",
            "",
        ])
        
        for rec in result.recommendations:
            lines.append(f"- {rec}")
        
        lines.extend(["", "---", ""])
    
    # Подвал отчёта
    lines.extend([
        "",
        "## ℹ️ О методологии",
        "",
        "Этот отчёт сгенерирован автоматически с использованием следующих индексов:",
        "",
        "- **Flesch Reading Ease** — основной индекс удобочитаемости (0-100)",
        "- **Flesch-Kincaid Grade** — уровень класса по американской системе",
        "- **Coleman-Liau Index** — индекс на основе длины слов и предложений",
        "- **ARI** — автоматический индекс читабельности",
        "",
        "Подробнее о формулах: [docs/formulas.md](../docs/formulas.md)",
        "",
        "---",
        "",
        f"*Сгенерировано: {datetime.now().isoformat()}*",
    ])
    
    return "\n".join(lines)


def main():
    """Главная функция скрипта."""
    args = parse_arguments()
    
    # Инициализация анализатора
    analyzer = TextAnalyzer(language=args.language)
    
    # Путь к директории с текстами
    input_dir = project_root / args.input_dir
    
    if not input_dir.exists():
        print(f"❌ Директория не найдена: {input_dir}")
        sys.exit(1)
    
    # Генерация отчёта
    print(f"📂 Анализ файлов в: {input_dir}")
    report = generate_report(analyzer, input_dir, args.language)
    
    # Сохранение отчёта
    output_path = project_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Отчёт сохранён: {output_path}")
    
    # Выводим краткую статистику
    txt_files = list(input_dir.glob("*.txt"))
    print(f"📊 Проанализировано файлов: {len(txt_files)}")


if __name__ == "__main__":
    main()