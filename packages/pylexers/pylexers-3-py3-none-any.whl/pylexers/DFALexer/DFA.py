from pylexers.RegularExpressions import _RegularExpression
from pylexers.RegularExpressions.BaseRegularExpressions import _EmptySet


class DFA:
    def __init__(self, regular_expression: _RegularExpression):
        alphabet = regular_expression.get_alphabet()
        self.states: dict[_RegularExpression, dict] = dict()
        queue = {regular_expression}
        while len(queue) > 0:
            current = queue.pop()
            if current in self.states:
                continue
            self.states[current] = dict()
            for symbol in alphabet:
                self.states[current][symbol] = current.derivative(symbol).simplify()
                queue.add(self.states[current][symbol])

        if _EmptySet() not in self.states.keys():
            self.states[_EmptySet()] = dict()

    def transition(self, state: _RegularExpression, symbol: chr):
        if state not in self.states:
            raise ValueError("Unknown State given to DFA")
        if symbol not in self.states[state]:
            return _EmptySet()
        return self.states[state][symbol]
