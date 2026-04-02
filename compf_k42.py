#!/usr/bin/env python3

from compf import Compf
from stack import Stack


class FormulaError(Exception):
    """
    Исключение для К42:
    содержит диагностику и корректную часть исходной формулы.
    """
    pass


class CompfK42(Compf):
    """
    К42:
    При компиляции неправильной формулы выдаётся диагностика об ошибке
    и корректная часть исходной формулы.
    """

    def __init__(self):
        super().__init__()

        # Исходный текст формулы
        self.text = ""

        # Текущая позиция во входной строке
        self.pos = 0

        # True  -> ожидаем операнд или '('
        # False -> ожидаем операцию или ')'
        self.need_value = True

    def compile(self, text):
        """
        Компиляция формулы в постфиксную запись
        с диагностикой синтаксических ошибок.
        """
        self.text = text
        self.pos = 0
        self.need_value = True

        # Очищаем структуры перед новым запуском
        self.data = []
        self.s = Stack()

        # Пустая формула
        if text == "":
            self.error("Пустая формула")

        # Разбираем исходную строку посимвольно
        for i, c in enumerate(text):
            self.pos = i
            self.process_symbol(c)

        # Если в конце всё ещё ждём операнд,
        # значит формула закончилась на операторе или '('
        if self.need_value:
            self.pos = len(text)
            self.error("Формула не может заканчиваться операцией")

        # Выгружаем оставшиеся операции из стека
        while self.s.array:
            top = self.s.top()

            # Если осталась открывающая скобка — ошибка
            if top == "(":
                self.pos = len(text)
                self.error("Не закрыта скобка")

            self.process_oper(self.s.pop())

        return " ".join(self.data)

    def process_symbol(self, c):
        """
        Обработка одного символа с контролем синтаксиса.
        """

        # Открывающая скобка
        if c == "(":
            # '(' допустима только там, где ожидается операнд
            if not self.need_value:
                self.error("Ожидалась операция")

            self.s.push(c)
            self.need_value = True
            return

        # Закрывающая скобка
        if c == ")":
            # ')' нельзя встретить, если ещё ждём операнд
            if self.need_value:
                self.error("Ожидался операнд")

            # Ищем соответствующую '('
            if "(" not in self.s.array:
                self.error("Лишняя закрывающая скобка")

            # Выгружаем операции до ближайшей '('
            while self.s.array and self.s.top() != "(":
                self.process_oper(self.s.pop())

            # Если вдруг '(' так и не нашли
            if not self.s.array:
                self.error("Лишняя закрывающая скобка")

            # Убираем '('
            self.s.pop()

            self.need_value = False
            return

        # Операция
        if c in "+-*/":
            # Операция допустима только после операнда/подвыражения
            if self.need_value:
                self.error("Ожидался операнд")

            # Выгружаем операции с большим или равным приоритетом
            while self.s.array and self.s.top() != "(" \
                    and self.is_precedes(self.s.top(), c):
                self.process_oper(self.s.pop())

            self.s.push(c)
            self.need_value = True
            return

        # Иначе должен быть допустимый операнд
        self.check_symbol(c)

        # Если операнд пришёл там, где ожидалась операция
        if not self.need_value:
            self.error("Ожидалась операция")

        self.process_value(c)
        self.need_value = False

    def error(self, message):
        """
        Формирование исключения с диагностикой и корректной частью.
        """
        correct_part = self.text[:self.pos]
        raise FormulaError(
            f"Ошибка в позиции {self.pos}: {message}. "
            f"Корректная часть: '{correct_part}'"
        )