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

    Базовый алгоритм разбора берём из Compf,
    но вместо обработки строки по символам
    сначала разбиваем её на токены.
    """

    def __init__(self):
        # Инициализация родительского класса:
        # создаётся стек операций self.s и список self.data
        super().__init__()

        # Стек числовых результатов, как в обычном Calc
        self.r = Stack()

        # Переменная d по условию изначально равна 0
        self.d = 0

    def compile(self, text):
        """
        Вычисление выражения по заданию И45.
        """

        # Перед каждым новым запуском очищаем состояние
        self.s = Stack()
        self.r = Stack()
        self.d = 0

        # Разбиваем строку на токены:
        # например d--*(2+d) -> ['d--', '*', '(', '2', '+', 'd', ')']
        tokens = self.tokenize(text)

        # Как и в Compf, искусственно добавляем внешние скобки,
        # чтобы все операции корректно вытолкнулись из стека
        for token in ["("] + tokens + [")"]:
            self.process_symbol(token)

        # В стеке результатов остаётся окончательный ответ
        return self.r.top()

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

            # Если встретили d, проверяем:
            # это просто d или конструкция d--
            elif c == 'd':
                if text[i:i + 3] == 'd--':
                    tokens.append('d--')
                    i += 3
                else:
                    tokens.append('d')
                    i += 1

            # Разрешённые бинарные операции и скобки
            elif c in '+*/()':
                tokens.append(c)
                i += 1

            # Обычное вычитание запрещено по условию И45
            elif c == '-':
                raise Exception("Операция вычитания в И45 не поддерживается")

            # Любой другой символ недопустим
            else:
                raise Exception(f"Недопустимый символ '{c}'")

        return tokens

    def process_symbol(self, token):
        """
        Обработка одного токена.

        Логика та же, что и в Compf:
        - '(' кладём в стек операций
        - ')' заставляет выполнить все отложенные операции до '('
        - оператор сначала выталкивает более приоритетные операции
        - операнд сразу обрабатывается
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

        Возможны три случая:
        1. Цифра
        2. Переменная d
        3. Постфиксная операция d--
        """
        if token.isdigit():
            self.r.push(int(token))

        elif token == 'd':
            # Просто кладём текущее значение d
            self.r.push(self.d)

        elif token == 'd--':
            # Постфиксный декремент:
            # сначала используем текущее значение d,
            # потом уменьшаем d на 1
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

        '+' имеет меньший приоритет,
        '*' и '/' имеют больший приоритет.
        """
        return 1 if c == "+" else 2