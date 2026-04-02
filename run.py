#!/usr/bin/env python3

from calc import Calc
from compf import Compf
from compf_k40 import CompfK40
from compf_k42 import CompfK42, FormulaError


def main():
    """
    Главный файл запуска проекта.

    Поддерживаются два режима:
    1. Формулы с буквами: проверка К42, затем Compf и К40
    2. Выражения с цифрами: вычисление через Calc
    """
    print("=== Демонстрация проекта ===")
    expr = input("Введите выражение: ")

    # Если во входной строке есть буквы,
    # считаем, что это формула для компилятора
    if any(ch.isalpha() for ch in expr):
        print("=== Режим компиляции формулы ===")

        # Сначала проверяем формулу через К42
        try:
            k42 = CompfK42()
            postfix_k42 = k42.compile(expr)
            print("К42: формула корректна")
            print("К42: постфиксная форма:", postfix_k42)
        except FormulaError as e:
            print("К42:", e)
            return

        # Если К42 ошибок не нашёл,
        # можно безопасно запускать обычный Compf
        compf = Compf()
        postfix = compf.compile(expr)
        print("Постфиксная форма:", postfix)

        # И К40
        k40 = CompfK40()
        full_expr = k40.compile(expr)
        print("К40: полностью скобочная форма:", full_expr)

    # Если во входной строке есть цифры,
    # считаем, что это арифметическое выражение
    elif any(ch.isdigit() for ch in expr):
        print("=== Режим вычисления ===")

        try:
            calc = Calc()
            result = calc.compile(expr)
            print("Результат:", result)
        except Exception as e:
            print("Ошибка вычисления:", e)

    else:
        print("Ошибка: введите формулу с буквами или выражение с цифрами.")


if __name__ == "__main__":
    main()