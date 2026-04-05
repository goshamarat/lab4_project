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

    # ----------------------------
    # Новые тесты для compile_with_d
    # ----------------------------

    # compile_with_d должен возвращать и результат, и итоговое значение d
    def test_compile_with_d_example1(self):
        result, d_value = self.c.compile_with_d('d--+d')
        assert result == -1
        assert d_value == -1

    def test_compile_with_d_example2(self):
        result, d_value = self.c.compile_with_d('d--*(2+d)')
        assert result == 0
        assert d_value == -1

    # После трёх d-- итоговое d должно стать -3
    def test_compile_with_d_several_decrements(self):
        result, d_value = self.c.compile_with_d('d--+d--+d--')
        assert result == -3
        assert d_value == -3

    # ----------------------------
    # Новые тесты на ошибки записи
    # ----------------------------

    # Нет операции между операндами
    def test_missing_operator_between_values(self):
        with raises(Exception):
            self.c.compile('1+2d--')

    # Две переменные подряд
    def test_two_values_in_row(self):
        with raises(Exception):
            self.c.compile('dd')

    # Нет операции перед скобкой
    def test_missing_operator_before_parenthesis(self):
        with raises(Exception):
            self.c.compile('2(d--+3)')

    # Нет операции после скобки
    def test_missing_operator_after_parenthesis(self):
        with raises(Exception):
            self.c.compile('(2+d)3')

    # Нет операции между скобками
    def test_missing_operator_between_parentheses(self):
        with raises(Exception):
            self.c.compile('(2+d)(3+d--)')

    # Два оператора подряд
    def test_double_operator(self):
        with raises(Exception):
            self.c.compile('2++3')

    # Оператор в начале выражения
    def test_operator_at_start(self):
        with raises(Exception):
            self.c.compile('+2')

    # Выражение заканчивается оператором
    def test_expression_ends_with_operator(self):
        with raises(Exception):
            self.c.compile('2+d--+')