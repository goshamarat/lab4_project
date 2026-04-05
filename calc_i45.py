#!/usr/bin/env python3

from compf import Compf
from stack import Stack


class CalcI45(Compf):
    """
    И45:
    Вычисление выражений, не содержащих операции вычитания,
    но содержащих:
    - цифры [0-9]
    - переменную d
    - постфиксную унарную операцию d--

    Особенности:
    1. Начальное значение d равно 0
    2. Символ d возвращает текущее значение переменной d
    3. Конструкция d-- возвращает текущее значение d,
       после чего уменьшает d на 1
    4. Обычное вычитание '-' запрещено
    5. Поддерживаются операции +, *, / и скобки
    """

    def __init__(self):
        super().__init__()
        self.r = Stack()
        self.d = 0

    def compile(self, text):
        """
        Старый совместимый интерфейс:
        возвращает только результат выражения.
        """
        result, _ = self.compile_with_d(text)
        return result

    def compile_with_d(self, text):
        """
        Новый метод:
        возвращает и результат, и итоговое значение d.
        """
        # Сбрасываем состояние перед каждым вычислением
        self.s = Stack()
        self.r = Stack()
        self.d = 0

        tokens = self.tokenize(text)

        # prev_type может быть:
        # None, 'value', 'op', '(', ')'
        prev_type = None

        for token in ["("] + tokens + [")"]:

            # Определяем тип текущего токена
#s            if token.isspace():
#                continue
            if self.is_value(token):
                current_type = 'value'
            elif token in "+*/":
                current_type = 'op'
            elif token == "(":
                current_type = '('
            elif token == ")":
                current_type = ')'
            else:
                raise Exception(f"Неизвестный токен '{token}'")

            # ----------------------------
            # Проверки корректности записи
            # ----------------------------

            # Два операнда подряд: 2d, dd, 2d--
            if prev_type == 'value' and current_type == 'value':
                raise Exception("Ошибка: нет операции между операндами")

            # Операнд сразу перед открывающей скобкой: 2(3+d)
            if prev_type == 'value' and current_type == '(':
                raise Exception("Ошибка: нет операции перед скобкой")

            # Закрывающая скобка сразу перед операндом: (2+3)4
            if prev_type == ')' and current_type == 'value':
                raise Exception("Ошибка: нет операции после скобки")

            # Закрывающая скобка сразу перед открывающей: )( или (2+3)(4+d)
            if prev_type == ')' and current_type == '(':
                raise Exception("Ошибка: нет операции между скобками")

            # Оператор в начале или сразу после открывающей скобки
            if current_type == 'op' and (prev_type is None or prev_type == '('):
                raise Exception("Ошибка: оператор в неверном месте")

            # Два оператора подряд
            if prev_type == 'op' and current_type == 'op':
                raise Exception("Ошибка: два оператора подряд")

            # Закрывающая скобка сразу после оператора: (2+)
            if prev_type == 'op' and current_type == ')':
                raise Exception("Ошибка: выражение заканчивается оператором")

            prev_type = current_type
            self.process_symbol(token)

        # После вычисления в стеке должен остаться ровно один результат
        if len(self.r.array) == 0:
            raise Exception("Ошибка: пустое выражение")

        result = self.r.pop()

        if len(self.r.array) != 0:
            raise Exception("Ошибка: лишние операнды в выражении")

        return result, self.d

    def tokenize(self, text):
        """
        Разбиение входной строки на токены.

        Допустимы:
        - цифры: 0..9
        - d
        - d--
        - операции + * /
        - скобки ( )
        - пробелы

        Обычное вычитание '-' запрещено.
        """
        tokens = []
        i = 0

        while i < len(text):
            c = text[i]

            # Пробелы игнорируем
            if c.isspace():
                i += 1

            # Цифра — отдельный токен
            elif c.isdigit():
                tokens.append(c)
                i += 1

            # d или d--
            elif c == 'd':
                if text[i:i + 3] == 'd--':
                    tokens.append('d--')
                    i += 3
                else:
                    tokens.append('d')
                    i += 1

            # Разрешённые операции и скобки
            elif c in '+*/()':
                tokens.append(c)
                i += 1

            # Обычное вычитание запрещено
            elif c == '-':
                raise Exception("Операция вычитания в И45 не поддерживается")

            # Всё остальное запрещено
            else:
                raise Exception(f"Недопустимый символ '{c}'")

        return tokens

    def is_value(self, token):
        """
        Проверка: является ли токен операндом.
        """
        return token.isdigit() or token in ('d', 'd--')

    def process_symbol(self, token):
        """
        Обработка одного токена.
        """
        if token == "(":
            self.s.push(token)

        elif token == ")":
            self.process_suspended_operators(token)
            self.s.pop()

        elif token in "+*/":
            self.process_suspended_operators(token)
            self.s.push(token)

        else:
            self.process_value(token)

    def process_value(self, token):
        """
        Обработка операнда.
        """
        if token.isdigit():
            self.r.push(int(token))

        elif token == 'd':
            self.r.push(self.d)

        elif token == 'd--':
            self.r.push(self.d)
            self.d -= 1

        else:
            raise Exception(f"Неизвестный операнд '{token}'")

    def process_oper(self, c):
        """
        Обработка бинарной операции.
        """
        second = self.r.pop()
        first = self.r.pop()

        if c == '+':
            self.r.push(first + second)
        elif c == '*':
            self.r.push(first * second)
        elif c == '/':
            self.r.push(first / second)

    @staticmethod
    def priority(c):
        """
        Приоритет операций.
        """
        return 1 if c == "+" else 2