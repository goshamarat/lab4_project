import os
import sys

# Добавляем в sys.path корневую папку проекта,
# чтобы тест мог импортировать файлы из lab4_project
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from compf_k40 import CompfK40


class TestCompfK40:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.c = CompfK40()

    # Формула из одного символа
    def test_one_symbol(self):
        assert self.c.compile("a") == "a"

    # Формулы с одной операцией
    def test_correct_operations1(self):
        assert self.c.compile("a+b") == "(a+b)"

    def test_correct_operations2(self):
        assert self.c.compile("a-b") == "(a-b)"

    def test_correct_operations3(self):
        assert self.c.compile("a*b") == "(a*b)"

    def test_correct_operations4(self):
        assert self.c.compile("a/b") == "(a/b)"

    # Тесты на порядок выполнения операций
    def test_operations_order1(self):
        assert self.c.compile("a+c*b") == "(a+(c*b))"

    def test_operations_order2(self):
        assert self.c.compile("a*b/c") == "((a*b)/c)"

    def test_operations_order3(self):
        assert self.c.compile("a*(b/c)") == "(a*(b/c))"

    # Тесты на использование скобок
    def test_parentheses1(self):
        assert self.c.compile("(a)") == "a"

    def test_parentheses2(self):
        assert self.c.compile("(((((a))))") == "a"

    def test_parentheses3(self):
        assert self.c.compile("(((((a+b))))") == "(a+b)"

    def test_parentheses4(self):
        assert self.c.compile("(((((((a+b)*((a+b)))))))") == "((a+b)*(a+b))"

    # Сложные выражения
    def test_expressions1(self):
        assert self.c.compile("(a+b)*c+(d-e)/f") == "(((a+b)*c)+((d-e)/f))"

    def test_expressions2(self):
        assert self.c.compile("a/b*c+d*e/(f+g)") == "(((a/b)*c)+((d*e)/(f+g)))"

    def test_expressions3(self):
        assert self.c.compile("a/b*(c+d*e)/(f+g)") == "(((a/b)*(c+(d*e)))/(f+g))"

    def test_expressions4(self):
        assert self.c.compile("a+b*(c-d)*(c+((d-e)/a))/a") == \
            "(a+(((b*(c-d))*(c+((d-e)/a)))/a))"