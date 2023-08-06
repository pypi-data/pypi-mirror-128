from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class _RegularExpression:
    type: str
    re1: Union["_RegularExpression", str, None] = None
    re2: Optional["_RegularExpression"] = None

    def is_empty_set(self) -> bool:
        return self.type == "EMPTY SET"

    def is_epsilon(self) -> bool:
        return self.type == "EPSILON"

    def is_symbol(self) -> bool:
        return self.type == "SYMBOL"

    def is_concat(self) -> bool:
        return self.type == "CONCAT"

    def is_or(self) -> bool:
        return self.type == "OR"

    def is_kleene_star(self) -> bool:
        return self.type == "KLEENE STAR"

    def is_nullable(self):
        return self.nullable().is_epsilon()

    def nullable(self) -> "_RegularExpression":
        if self.is_epsilon() or self.is_kleene_star():
            return _Epsilon()
        elif self.is_empty_set() or self.is_symbol():
            return _EmptySet()
        elif self.is_concat():
            a = self.re1.nullable()
            b = self.re2.nullable()
            if a.is_epsilon() and b.is_epsilon():
                return _Epsilon()
            return _EmptySet()
        elif self.is_or():
            a = self.re1.nullable()
            b = self.re2.nullable()
            if a.is_epsilon() or b.is_epsilon():
                return _Epsilon()
            return _EmptySet()

    def simplify(self) -> "_RegularExpression":
        if self.is_concat():
            r = self.re1.simplify()
            s = self.re2.simplify()
            if r.is_empty_set() or s.is_empty_set():
                return _EmptySet()
            if r.is_epsilon():
                return s
            if s.is_epsilon():
                return r
        elif self.is_or():
            r = self.re1.simplify()
            s = self.re2.simplify()
            if r.is_empty_set():
                return s
            elif s.is_empty_set():
                return r
        return self

    def derivative(self, symbol) -> "_RegularExpression":
        if self.is_empty_set() or self.is_epsilon():
            return _EmptySet()
        elif self.is_symbol():
            if self.re1 == symbol:
                return _Epsilon()
            else:
                return _EmptySet()
        elif self.is_concat():
            dr = self.re1.derivative(symbol)
            ds = self.re2.derivative(symbol)
            return _Or(
                _Concat(dr, self.re2), _Concat(self.re1.nullable(), ds)
            ).simplify()
        elif self.is_or():
            dr = self.re1.derivative(symbol)
            ds = self.re2.derivative(symbol)
            return _Or(dr, ds).simplify()
        elif self.is_kleene_star():
            dr = self.re1.derivative(symbol)
            return _Concat(dr, self).simplify()
        else:
            raise SyntaxError("Encountered unknown regular expession")

    def matches(self, string):
        re = self
        for c in string:
            re = re.derivative(c).simplify()
        return re.is_nullable()

    def get_alphabet(self) -> str:
        if self.re1 and self.re2:
            return self.re1.get_alphabet() + self.re2.get_alphabet()
        elif isinstance(self.re1, _RegularExpression):
            return self.re1.get_alphabet()
        else:
            return self.re1 or ""


class _EmptySet(_RegularExpression):
    def __init__(self):
        super().__init__("EMPTY SET")


class _Epsilon(_RegularExpression):
    def __init__(self):
        super().__init__("EPSILON")


class _Symbol(_RegularExpression):
    def __init__(self, symbol: str):
        super().__init__("SYMBOL", symbol)


class _Concat(_RegularExpression):
    def __init__(
        self,
        regular_expression_1: _RegularExpression,
        regular_expression_2: _RegularExpression,
    ):
        super().__init__("CONCAT", regular_expression_1, regular_expression_2)


class _Or(_RegularExpression):
    def __init__(
        self,
        regular_expression_1: _RegularExpression,
        regular_expression_2: _RegularExpression,
    ):
        super().__init__("OR", regular_expression_1, regular_expression_2)


class _Star(_RegularExpression):
    def __init__(
        self,
        regular_expression: _RegularExpression,
    ):
        super().__init__("KLEENE STAR", regular_expression)


def _get_regular_expression_arg1(re: _RegularExpression) -> _RegularExpression:
    return re.re1 or _EmptySet()


def _get_regular_expression_arg2(re: _RegularExpression) -> _RegularExpression:
    return re.re2 or _EmptySet()
