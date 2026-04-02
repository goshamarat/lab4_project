from pytest import raises
from compf_k42 import CompfK42, FormulaError


class TestCompfK42:

    # Инициализация перед каждым тестом
    def setup_method(self):
        self.c = CompfK42()

    # ----------------------------
    # Корректные формулы
    # ----------------------------

    def test_one_symbol(self):
        assert self.c.compile("a") == "a"

    def test_simple_add(self):
        assert self.c.compile("a+b") == "a b +"

    def test_simple_sub(self):
        assert self.c.compile("a-b") == "a b -"

    def test_simple_mul(self):
        assert self.c.compile("a*b") == "a b *"

    def test_simple_div(self):
        assert self.c.compile("a/b") == "a b /"

    def test_priority(self):
        assert self.c.compile("a+b*c") == "a b c * +"

    def test_parentheses(self):
        assert self.c.compile("(a+b)*c") == "a b + c *"

    def test_complex_expression(self):
        assert self.c.compile("a/b*(c+d*e)/(f+g)") == \
            "a b / c d e * + * f g + /"

    # ----------------------------
    # Ошибки
    # ----------------------------

    # Пустая строка
    def test_empty_string(self):
        with raises(FormulaError) as exc:
            self.c.compile("")
        assert "Пустая формула" in str(exc.value)
        assert "Корректная часть: ''" in str(exc.value)

    # Формула начинается с операции
    def test_starts_with_operator(self):
        with raises(FormulaError) as exc:
            self.c.compile("+a")
        assert "Ожидался операнд" in str(exc.value)
        assert "Корректная часть: ''" in str(exc.value)

    # Формула заканчивается операцией
    def test_ends_with_operator(self):
        with raises(FormulaError) as exc:
            self.c.compile("a+")
        assert "Формула не может заканчиваться операцией" in str(exc.value)
        assert "Корректная часть: 'a+'" in str(exc.value)

    # Две операции подряд
    def test_double_operator(self):
        with raises(FormulaError) as exc:
            self.c.compile("a++b")
        assert "Ожидался операнд" in str(exc.value)
        assert "Корректная часть: 'a+'" in str(exc.value)

    # Два операнда подряд
    def test_two_values_in_row(self):
        with raises(FormulaError) as exc:
            self.c.compile("ab")
        assert "Ожидалась операция" in str(exc.value)
        assert "Корректная часть: 'a'" in str(exc.value)

    # Неявное умножение недопустимо
    def test_value_before_parenthesis(self):
        with raises(FormulaError) as exc:
            self.c.compile("a(b+c)")
        assert "Ожидалась операция" in str(exc.value)
        assert "Корректная часть: 'a'" in str(exc.value)

    # Пустые скобки
    def test_empty_parentheses(self):
        with raises(FormulaError) as exc:
            self.c.compile("a+()")
        assert "Ожидался операнд" in str(exc.value)
        assert "Корректная часть: 'a+('" in str(exc.value)

    # Лишняя закрывающая скобка
    def test_extra_closing_parenthesis(self):
        with raises(FormulaError) as exc:
            self.c.compile("a+b)")
        assert "Лишняя закрывающая скобка" in str(exc.value) \
            or "Ожидалась операция" in str(exc.value)

    # Незакрытая скобка
    def test_unclosed_parenthesis(self):
        with raises(FormulaError) as exc:
            self.c.compile("(a+b")
        assert "Не закрыта скобка" in str(exc.value)

    # Формула заканчивается на открывающую скобку
    def test_ends_with_open_parenthesis(self):
        with raises(FormulaError) as exc:
            self.c.compile("a+(")
        assert "Формула не может заканчиваться операцией" in str(exc.value)
        assert "Корректная часть: 'a+('" in str(exc.value)

    # Недопустимый символ
    def test_invalid_symbol(self):
        with raises(Exception) as exc:
            self.c.compile("a+$")
        assert "Недопустимый символ" in str(exc.value)