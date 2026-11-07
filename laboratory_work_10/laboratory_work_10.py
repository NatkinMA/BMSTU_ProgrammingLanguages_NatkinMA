"""main.py — точка входа лексического анализатора языка «Бауманец».

Запуск:
    python3 main.py <путь_к_файлу>

Читает исходный файл, запускает лексер и печатает таблицу токенов.
При лексической ошибке выводит сообщение с позицией и завершается
с кодом возврата 1. Разбор не прерывается на первой ошибке — файл
просматривается целиком (см. раздел 3 методички).
"""

import sys
from pathlib import Path

from tokens import Token
from lexer import Lexer

SEPARATOR = "—"


def print_token_table(tokens: list[Token]) -> None:
    """Печатает таблицу токенов в выровненном виде."""
    header = f"{'№':>4}  {'Тип':<8}  {'Значение':<30}  {'Строка':>6}  {'Столбец':>7}"
    print(header)
    print(SEPARATOR * len(header))
    for number, token in enumerate(tokens, start=1):
        print(
            f"{number:>4}  {token.type:<8}  {token.value:<30}  "
            f"{token.line:>6}  {token.col:>7}"
        )

source_path = Path("programm.bmstu")

try:
    source = source_path.read_text(encoding="utf-8")
    print(source_path)
    print(source)
    tokens = Lexer(source).tokenize()
    print_token_table(tokens)
except OSError as error:
    print(f"Ошибка чтения файла: {error}", file=sys.stderr)
