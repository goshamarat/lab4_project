#!/usr/bin/env python3

import subprocess
import sys
from collections import Counter

from calc import Calc
from calc_i45 import CalcI45
from compf import Compf
from compf_k40 import CompfK40
from compf_k42 import CompfK42, FormulaError


def print_header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_block(title):
    print(f"\n--- {title} ---")


def run_tests():
    """
    Запуск всех тестов проекта через pytest
    с красивым стандартным выводом и статистикой по блокам.
    """
    print_header("ЗАПУСК ТЕСТОВ")

    try:
        # Первый запуск: обычный красивый вывод pytest
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"],
            text=True
        )

        # Второй запуск: тихо собираем список тестов для подсчёта по блокам
        collect = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            text=True,
            capture_output=True
        )

        test_counts = Counter()

        for line in collect.stdout.splitlines():
            line = line.strip()

            if line.startswith("tests/test_calc.py::"):
                test_counts["Calc"] += 1
            elif line.startswith("tests/test_calc_i45.py::"):
                test_counts["I45"] += 1
            elif line.startswith("tests/test_compf.py::"):
                test_counts["Compf"] += 1
            elif line.startswith("tests/test_compf_k40.py::"):
                test_counts["K40"] += 1
            elif line.startswith("tests/test_compf_k42.py::"):
                test_counts["K42"] += 1
            elif line.startswith("tests/test_stack.py::"):
                test_counts["Stack"] += 1

        ordered_blocks = [
            "Calc",
            "I45",
            "Compf",
            "K40",
            "K42",
            "Stack"
        ]

        total_tests = sum(test_counts.values())

        if result.returncode == 0:
            print("\nВсе тесты успешно пройдены.")
        else:
            print("\nНекоторые тесты завершились с ошибками.")

        print_block("Статистика по блокам")
        for block in ordered_blocks:
            print(f"{block:<10}: {test_counts.get(block, 0)}")

        print(f"\nВсего тестов: {total_tests}")

    except FileNotFoundError:
        print("\npytest не найден. Установите его командой:")
        print("sudo apt install pytest")


def run_formula_mode(expr):
    """
    Режим компиляции формулы с буквами.
    """
    print_header("РЕЖИМ КОМПИЛЯЦИИ ФОРМУЛЫ")

    try:
        k42 = CompfK42()
        k42.compile(expr)
        print("К42: формула корректна")
    except FormulaError as e:
        print(f"К42: {e}")
        return

    compf = Compf()
    postfix = compf.compile(expr)

    k40 = CompfK40()
    full_expr = k40.compile(expr)

    print_block("Результаты")
    print(f"Исходная формула           : {expr}")
    print(f"Постфиксная форма          : {postfix}")
    print(f"Полностью скобочная форма  : {full_expr}")


def run_calc_mode(expr):
    """
    Режим вычисления обычного арифметического выражения.
    """
    print_header("РЕЖИМ ВЫЧИСЛЕНИЯ")

    try:
        calc = Calc()
        result = calc.compile(expr)

        print_block("Результаты")
        print(f"Исходное выражение : {expr}")
        print(f"Результат          : {result}")

    except Exception as e:
        print(f"Ошибка вычисления! {e}")


def run_calc_i45_mode(expr):
    """
    Режим вычисления выражения по заданию И45.
    """
    print_header("РЕЖИМ ВЫЧИСЛЕНИЯ И45")

    try:
        calc = CalcI45()
        result = calc.compile(expr)

        print_block("Результаты")
        print(f"Исходное выражение : {expr}")
        print(f"Результат          : {result}")

    except Exception as e:
        print(f"Ошибка вычисления И45! {e}")


def main():
    print_header("ДЕМОНСТРАЦИЯ ПРОЕКТА")

    answer = input("Запустить тесты перед началом? (y/n): ").strip().lower()
    if answer == "y":
        run_tests()

    print_header("ОСНОВНОЙ ЗАПУСК")
    expr = input("Введите выражение: ").strip()

    # Разрешённые символы для И45
    allowed_i45_chars = set("0123456789d+*/()- ")

    if set(expr) <= allowed_i45_chars and 'd' in expr:
        run_calc_i45_mode(expr)
    elif any(ch.isalpha() for ch in expr):
        run_formula_mode(expr)
    elif any(ch.isdigit() for ch in expr):
        run_calc_mode(expr)
    else:
        print("Ошибка: введите корректное выражение.")


if __name__ == "__main__":
    main()