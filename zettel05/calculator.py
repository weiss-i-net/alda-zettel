import doctest
import pytest

class SyntaxTree:
    """Creates, stores and evaluates a binary tree reprensation of an arithmitic expression.

    >>> a = SyntaxTree('(2*1-2*1+4)/2')
    >>> a.evaluate()
    2.0
    """

    def __init__(self, exp_str):
        self._root = SyntaxTree._parse_string(exp_str)

    def evaluate(self):
        """Evaluate the internal expression-tree and return the result as float.

        >>> a = SyntaxTree('2*4*(3+(4-7)*8)-(1-6)')
        >>> a.evaluate()
        -163
        """
        return SyntaxTree._evaluate_node(self._root)


    class _Operator:
        def __init__(self):
            self._op = ''
            self._right = self._left = None

    class _Number:
        def __init__(self, value):
            self._value = float(value)

    @staticmethod
    def _skip_parenthesis(exp_str, index):
        """If exp_str[index] is a parenthesis, return the index of the matching parenthesis.

        >>> SyntaxTree._skip_parenthesis("a(b(cd)e)fg", 1)
        8
        """
        # determine direction
        walking_right = True if exp_str[index] == '(' else False

        parenth_count = 0
        while True:
            parenth_count += 1 if exp_str[index] == '(' else (
                            -1 if exp_str[index] == ')' else (
                             0 ))

            # if parenth_count is 0 each opening parenthesis has been matched with a closing one
            if parenth_count == 0:
                return index

            index += 1 if walking_right else -1

            # Error if end is reached with unmatched parenthesis
            if index in (-1, len(exp_str)):
                raise ValueError(f'Encountered unmatched parenthesis in {exp_str}')

    @staticmethod
    def _parse_string(exp_str):
        exp_str_len = len(exp_str)

        # remove eventual enclosing parenthesis
        if SyntaxTree._skip_parenthesis(exp_str, 0) == exp_str_len - 1 and exp_str_len > 1:
            exp_str = exp_str[1:-1]
            exp_str_len -= 2

        next_op = ('/', '*')

        # check if top-level exp includes + or -
        index = 0
        while index < exp_str_len:
            char = exp_str[index]

            if char == '(':
                index = SyntaxTree._skip_parenthesis(exp_str, index)
            elif char in ('+', '-'):
                next_op = ('+', '-')

            index += 1

        # find last occurrence of next_op (which is the lowest precedence operation)
        index = exp_str_len - 1
        while index >= 0:
            char = exp_str[index]

            if char == ')':
                index = SyntaxTree._skip_parenthesis(exp_str, index)

            elif char in next_op:
                # if op has been found recursively call _parse_string on both sides
                node = SyntaxTree._Operator()
                node._op = char
                node._left = SyntaxTree._parse_string(exp_str[:index])
                node._right = SyntaxTree._parse_string(exp_str[index+1:])
                return node

            index -= 1

        # if no op is found exp_string is a number
        return SyntaxTree._Number(exp_str)

    @staticmethod
    def _evaluate_node(node):
        # check if node is number
        if isinstance(node, SyntaxTree._Number):
            return node._value

        # if not calculate left (op) right
        op = node._op
        if op == '+':
            return SyntaxTree._evaluate_node(node._left) + SyntaxTree._evaluate_node(node._right)
        if op == '-':
            return SyntaxTree._evaluate_node(node._left) - SyntaxTree._evaluate_node(node._right)
        if op == '*':
            return SyntaxTree._evaluate_node(node._left) * SyntaxTree._evaluate_node(node._right)
        if op == '/':
            return SyntaxTree._evaluate_node(node._left) / SyntaxTree._evaluate_node(node._right)



################################################################################
#                                Testing                                       #
################################################################################

def test_skip_parenthesis():
    # forward skipping
    assert SyntaxTree._skip_parenthesis("(abcde)", 0) == 6
    assert SyntaxTree._skip_parenthesis("(abc)de", 0) == 4
    assert SyntaxTree._skip_parenthesis("ab(cde)", 2) == 6
    assert SyntaxTree._skip_parenthesis("(()(d))", 0) == 6

    # backward skipping
    assert SyntaxTree._skip_parenthesis("(abcde)", 6) == 0
    assert SyntaxTree._skip_parenthesis("(abc)de", 4) == 0
    assert SyntaxTree._skip_parenthesis("ab(cde)", 6) == 2
    assert SyntaxTree._skip_parenthesis("(()(d))", 6) == 0

    # no skipping
    assert SyntaxTree._skip_parenthesis("(abc)de", 2) == 2
    assert SyntaxTree._skip_parenthesis("(abc)de", 6) == 6
    assert SyntaxTree._skip_parenthesis("ab(c)de", 0) == 0
    assert SyntaxTree._skip_parenthesis("(()(d))", 4) == 4

    # no match found
    with pytest.raises(ValueError):
        SyntaxTree._skip_parenthesis("(abcdef", 0)
    with pytest.raises(ValueError):
        SyntaxTree._skip_parenthesis("abc)def", 3)

def test_operator_precedence():
    assert SyntaxTree('1+2-3*4/5').evaluate() == pytest.approx(0.6)
    assert SyntaxTree('1-3*4/5+2').evaluate() == pytest.approx(0.6)
    assert SyntaxTree('1-4/5*3+2').evaluate() == pytest.approx(0.6)

def test_parenthesis_precedence():
    assert SyntaxTree('(2+1)*3-1').evaluate() == pytest.approx(8)
    assert SyntaxTree('2-3*(2+1)').evaluate() == pytest.approx(-7)
    assert SyntaxTree('(9/3)+(2*3+1)-1').evaluate() == pytest.approx(9)

def test_parenthesis_nesting():
    assert SyntaxTree('(2*(1+2))*2').evaluate() == pytest.approx(12)
    assert SyntaxTree('(((2)*2+2)/2-2)').evaluate() == pytest.approx(1)
    assert SyntaxTree('(((2-1)+(0-1+1))-(4/2))*((10-8)/(0-2))').evaluate() == pytest.approx(1)

def test_unmatched_parenthesis():
    with pytest.raises(ValueError):
        SyntaxTree('1*(2/(3+4)))')
    with pytest.raises(ValueError):
        SyntaxTree('(1*(2-(3/4)')
    with pytest.raises(ValueError):
        SyntaxTree('(1-2)*(1+2)(')
    with pytest.raises(ValueError):
        SyntaxTree(')(1-2)*(1+2)(')

def test_docstring():
    doctest.testmod()
