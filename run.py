#!/usr/bin/env python3

from calc import Calc
from compf import Compf
from compf_k40 import CompfK40


def main():
    """
    Главный файл запуска проекта.

    Поддерживаются два режима:
    1. Формулы с буквами: компиляция в постфиксную форму и К40
    2. Выражения с цифрами: вычисление через Calc
    """
    print("=== Демонстрация проекта ===")
    expr = input("Введите выражение: ")

    # Если во входной строке есть буквы,
    # это формула для Compf и CompfK40.
    if any(ch.isalpha() for ch in expr):
        print("=== Режим компиляции формулы ===")

        compf = Compf()
        postfix = compf.compile(expr)
        print("Постфиксная форма:", postfix)

        k40 = CompfK40()
        full_expr = k40.compile(expr)
        print("Полностью скобочная форма:", full_expr)

    # Если во входной строке есть цифры,
    # это арифметическое выражение для Calc.
    elif any(ch.isdigit() for ch in expr):
        print("=== Режим вычисления ===")

        calc = Calc()
        result = calc.compile(expr)
        print("Результат:", result)

    # Во всех остальных случаях считаем ввод некорректным.
    else:
        print("Ошибка: введите формулу с буквами или выражение с цифрами.")


if __name__ == "__main__":
    main()