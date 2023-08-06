from pylexers.BaseLexer import Lexer
from pylexers.RegularExpressions.BaseRegularExpressions import _RegularExpression


class DerivativeLexer(Lexer):
    def get_successful_id(self, derivatives: list[_RegularExpression]):
        for index in range(len(derivatives)):
            if derivatives[index].nullable().is_epsilon():
                return index
        return True

    def is_failure_state(self, derivatives: list[_RegularExpression]):
        for derivative_ in derivatives:
            if not derivative_.simplify().is_empty_set():
                return False
        return True

    def find_records(self):
        i = self.i
        j = self.i
        records = []
        derivatives: list[_RegularExpression] = self.regular_expressions.copy()
        while len(self.source_program) > j:
            symbol = self.source_program[j]
            derivatives = [re.derivative(symbol) for re in derivatives]
            j = j + 1
            records += [[i, j, derivatives.copy()]]
            if self.is_failure_state(derivatives):
                break
        return records
