from string import printable

from pylexers.RegularExpressions.BaseRegularExpressions import (
    _EmptySet,
    _Epsilon,
    _Symbol,
    _Or,
    _Concat,
    _Star,
)

from pylexers.RegularExpressions.BaseRegularExpressions import _RegularExpression

"""
Basic Regular Expressions
"""


class EmptySet(_EmptySet):
    pass


class Epsilon(_Epsilon):
    pass


class Symbol(_Symbol):
    pass


def Or(*regular_expressions: _RegularExpression) -> _RegularExpression:
    re = regular_expressions[0]
    for r in regular_expressions[1:]:
        re = _Or(re, r)
    return re


def Concat(
    regular_expression_1: _RegularExpression, regular_expression_2: _RegularExpression
) -> _RegularExpression:
    return _Concat(regular_expression_1, regular_expression_2)


class Star(_Star):
    pass


"""
Extended Regular Expressions
"""


def Sigma(alphabet: str = printable, exclude: str = "") -> _RegularExpression:
    return Or(*[_Symbol(a) for a in alphabet if a not in exclude])


def String(string: str) -> _RegularExpression:
    if len(string) == 1:
        return _Symbol(string)
    return Concat(_Symbol(string[0]), String(string[1:]))


def AtLeastOne(regular_expression: _RegularExpression) -> _RegularExpression:
    return Concat(regular_expression, _Star(regular_expression))


def Optional(regular_expression: _RegularExpression) -> _RegularExpression:
    return _Or(regular_expression, _Epsilon())
