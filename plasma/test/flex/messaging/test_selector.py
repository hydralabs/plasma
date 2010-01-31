from nose.tools import raises

from plasma.flex.messaging.selector.parser import evaluate
from plasma.flex.messaging.selector import (LexerError, IncompatibleTypeError,
    UnknownVariableError, ParseError)


class TestInvalidChars(object):
    @raises(LexerError)
    def test_invalid_input(self):
        evaluate('true & false')


class TestSyntaxError(object):
    @raises(ParseError)
    def test_invalid_syntax(self):
        evaluate('2 > > 2')


class TestUndefinedVariable(object):
    @raises(UnknownVariableError)
    def test_undefined_variable(self):
        vars = {'var1': 'value'}
        evaluate('var1 = var2')


class TestEquality(object):
    def test_eq_string(self):
        vars = {'var1': r"\'test\'"}
        assert evaluate(r"'\'test\'' = var1", vars)

    def test_neq_string(self):
        vars = {'var1': r"\'test\'"}
        assert evaluate(r"'\'tset\'' <> var1", vars)


class TestComparisons(object):
    @raises(IncompatibleTypeError)
    def test_invalid_gt_operands(self):
        vars = {'var1': 'text', 'var2': 0}
        evaluate('var1 > var2', vars)

    def test_gt_false(self):
        assert not evaluate('2 > 3')

    def test_gt_true(self):
        assert evaluate('2 > 1')

    def test_gte_false(self):
        assert not evaluate('2 >= 3')

    def test_gte_true(self):
        assert evaluate('2 >= 2')

    def test_lt_false(self):
        assert not evaluate('3 < 2')

    def test_lt_true(self):
        assert evaluate('1 < 2')

    def test_lte_false(self):
        assert not evaluate('3 <= 2')

    def test_lte_true(self):
        assert evaluate('2 <= 2')


class TestArithmetic(object):
    @raises(IncompatibleTypeError)
    def test_arithmetic_invalid_operands(self):
        vars = {'var1': 1, 'var2': '2'}
        evaluate('var1 + var2', vars)

    def test_add(self):
        assert evaluate('1 + 2 = 3')
        assert evaluate('1.5 + .5 = 2')
        assert evaluate('0xff + 0x10 = 0x10F')

    def test_deduce(self):
        assert evaluate('3 - 2 = 1')
        assert evaluate('3e2 - 200 = 100')

    def test_product(self):
        assert evaluate('3 * 2 = 6')
        assert evaluate('5e+2 * 2 = 1000')

    def test_division(self):
        assert evaluate('6 / 3 = 2')
        assert evaluate('2e-2 * 2 = 0.04')

    def test_precedence(self):
        assert evaluate('3 + 4 * 4 = 19')

    def test_unary_minus(self):
        assert evaluate('2 * -5 = -10')

    @raises(IncompatibleTypeError)
    def test_invalid_unary_minus(self):
        evaluate("-'test'")


class TestParentheses(object):
    def test_num_paren(self):
        assert evaluate('(9 + 10) = (2 * 9 + 1)')

    def test_bool_paren(self):
        assert not evaluate('(true = true) = (true = false)')


class TestLogicalOperators(object):
    @raises(IncompatibleTypeError)
    def test_and_invalid_operands(self):
        vars = {'var1': 1, 'var2': 0}
        evaluate('var1 and var2', vars)

    def test_and_vars(self):
        vars = {'var1': True, 'var2': True}
        assert evaluate('var1 and var2', vars)
        vars['var2'] = False
        assert not evaluate('var1 and var2', vars)

    def test_and_numbers(self):
        assert evaluate('1 + 2 = 3 and 5 - 4 = 1')
        assert not evaluate('1 + 5 = 6 and 6 - 5 = 2')

    def test_and_num_vars(self):
        vars = {'var1': 3, 'var2': 7}
        assert evaluate('var1 + 5 = 8 and 9 - var2 = 2', vars)

    def test_or_vars(self):
        vars = {'var1': True, 'var2': False}
        assert evaluate('var1 or var2', vars)
        vars['var1'] = False
        assert not evaluate('var1 or var2', vars)

    def test_or_numbers(self):
        assert evaluate('2 + 5 = 8 or 3 + 6 = 9')
        assert not evaluate('7 + 0 = 8 or 4 - 3 = 2')


class TestBetween(object):
    @raises(IncompatibleTypeError)
    def test_between_invalid_operands(self):
        vars = {'var1': 'test', 'var2': 0}
        evaluate('var1 between 1 and var2', vars)

    @raises(IncompatibleTypeError)
    def test_not_between_invalid_operands(self):
        vars = {'var1': 'test', 'var2': 0}
        evaluate('var1 not between 1 and var2', vars)

    def test_between(self):
        assert evaluate('4 between 2 and 6')
        assert not evaluate('4 between 5 and 8')

    def test_not_between(self):
        assert evaluate('8 not between 3 and 5')
        assert not evaluate('8 not between 3 and 9')


class TestIs(object):
    def test_isnull(self):
        assert evaluate('somevar is null')
        assert not evaluate('somevar is not null')

    def test_notnull(self):
        vars = {'somevar': u'value'}
        assert not evaluate('somevar is null', vars)
        assert evaluate('somevar is not null', vars)


class TestIn(object):
    def test_in(self):
        vars = {'var1': 'abc', 'var2': 'xyz'}
        assert evaluate("'xyz' in (var1, 'def', var2)", vars)
        assert not evaluate("'ghi' in (var1, 'def', var2)", vars)

    def test_not_in(self):
        vars = {'var1': 'xxx', 'var2': 'yyy'}
        assert evaluate("'xyz' not in (var1, 'def', var2)", vars)
        assert not evaluate("'yyy' not in (var1, 'def', var2)", vars)


class TestLike(object):
    def test_like_simple(self):
        assert evaluate("'abc' like 'abc'")

    def test_like_wildcard(self):
        vars = {'var1': 'my test string'}
        assert evaluate("var1 like '%est%'", vars)
        assert not evaluate("var1 like 'est'", vars)
        assert not evaluate("var1 like '%est'", vars)
        assert not evaluate("var1 like 'est%'", vars)

    def test_like_tricks(self):
        assert evaluate("'x' like '_%'")
        assert evaluate("'x' like '%'")
        assert evaluate("'x' like '%%'")

    def test_like_empty_source(self):
        assert evaluate("'' like '%'")
        assert not evaluate("'' like '_%'")

    def test_like_escape(self):
        assert evaluate(r"'\nx%_\n\\' like '\nx\%\_\n\\'")

    def test_like_alternate_escape(self):
        assert evaluate(r"'\nx%_\n\\' like '\nx*%*_\n\\' escape '*'")

    @raises(IncompatibleTypeError)
    def test_invalid_like_operands(self):
        vars = {'var1': 'text', 'var2': 0}
        evaluate('var1 like var2', vars)

    def test_not_like(self):
        vars = {'var1': 'my test string'}
        assert evaluate("var1 not like '%stringe'", vars)
        assert evaluate("var1 not like ' my str%'", vars)

    @raises(IncompatibleTypeError)
    def test_invalid_not_like_operands(self):
        vars = {'var1': 'text', 'var2': 0}
        evaluate('var1 not like var2', vars)
