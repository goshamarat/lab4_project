from pytest import approx, raises
from calc_i45 import CalcI45


class TestCalcI45:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.c = CalcI45()

    # Обычная цифра вычисляется как сама себя
    def test_digit(self):
        assert self.c.compile('7') == 7

    # Переменная d по условию изначально равна 0
    def test_plain_d(self):
        assert self.c.compile('d') == 0

    # Постфиксный декремент:
    # сначала возвращается текущее значение d, потом d уменьшается
    def test_postfix_decrement(self):
        assert self.c.compile('d--') == 0

    # Пример из задания:
    # d = 0
    # d-- -> 0, потом d = -1
    # (2 + d) = 1
    # 0 * 1 = 0
    def test_task_example1(self):
        assert self.c.compile('d--*(2+d)') == 0

    # Пример из задания:
    # d-- -> 0, потом d = -1
    # d -> -1
    # 0 + (-1) = -1
    def test_task_example2(self):
        assert self.c.compile('d--+d') == -1

    # Несколько последовательных декрементов
    # d-- -> 0
    # d-- -> -1
    # d-- -> -2
    # Сумма: -3
    def test_several_decrements(self):
        assert self.c.compile('d--+d--+d--') == -3

    # Смешанное использование d и d--
    # d -> 0
    # d-- -> 0, потом d = -1
    # d -> -1
    # Сумма: -1
    def test_mix_d_and_ddec(self):
        assert self.c.compile('d+d--+d') == -1

    # Проверка приоритета операций:
    # d-- сначала даёт 0, потом d = -1
    # 0 * 3 = 0
    # 2 + 0 = 2
    def test_priority(self):
        assert self.c.compile('2+d--*3') == 2

    # Проверка работы скобок
    # d-- -> 0, потом d = -1
    # (0 + 2) * (-1 + 3) = 2 * 2 = 4
    def test_parentheses(self):
        assert self.c.compile('(d--+2)*(d+3)') == approx(4)

    # Проверка деления
    # d-- -> 0, потом d = -1
    # (8 + 0) / (2 + (-1)) = 8 / 1 = 8
    def test_division(self):
        assert self.c.compile('(8+d--)/(2+d)') == approx(8)

    # Пробелы во входной строке не должны мешать вычислению
    def test_spaces(self):
        assert self.c.compile(' d-- * ( 2 + d ) ') == 0

    # Обычное вычитание по условию запрещено
    def test_subtraction_is_forbidden(self):
        with raises(Exception):
            self.c.compile('1-2')

    # Недопустимые символы должны вызывать ошибку
    def test_invalid_symbol(self):
        with raises(Exception):
            self.c.compile('d--+x')