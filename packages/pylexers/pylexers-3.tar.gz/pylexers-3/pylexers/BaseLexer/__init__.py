from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")


@dataclass(frozen=True)
class Token(Generic[T]):
    identifier: str
    lexeme: str
    value: T


def build_token_func(
    identifier: str, process_lexeme_func: Optional[Callable[[str], T]] = None
) -> Callable[[str], Token[T]]:
    if process_lexeme_func:
        return lambda lexeme: Token(identifier, lexeme, process_lexeme_func(lexeme))
    return lambda lexeme: Token(identifier, lexeme, None)


class Lexer:
    def __init__(self, regular_expressions: list, tokenize_functions: list):
        self.regular_expressions = regular_expressions
        self.tokenize_functions = tokenize_functions
        self.source_program = ""
        if len(regular_expressions) != len(tokenize_functions):
            raise SyntaxError(
                f"Regular Expressions{len(regular_expressions)} and "
                f"Tokenizeing functions{len(tokenize_functions)} are "
                f"not the same length"
            )

    def set_source_program(self, source_program) -> iter:
        self.source_program = source_program
        return iter(self)

    def find_records(self) -> list:
        return []

    def get_successful_id(self, states) -> int:
        return -1

    def is_failure_state(self, derivatives) -> bool:
        return True

    def __iter__(self, **kwargs):
        self.i = 0
        return self

    def __next__(self):
        while True:
            if len(self.source_program) <= self.i:
                raise StopIteration
            records = self.find_records()
            for record in records[::-1]:
                if not self.is_failure_state(record[2]):
                    lexeme = self.source_program[record[0] : record[1]]
                    token_function_id = self.get_successful_id(record[2])
                    self.i = record[1]
                    token = self.tokenize_functions[token_function_id](lexeme)
                    if token is not None:
                        return token
                    else:
                        break

    def peek(self, n=1):
        original_i = self.i
        while True:
            if len(self.source_program) <= self.i:
                return None
            records = self.find_records()
            for record in records[::-1]:
                if not self.is_failure_state(record[2]):
                    lexeme = self.source_program[record[0] : record[1]]
                    token_function_id = self.get_successful_id(record[2])
                    token = self.tokenize_functions[token_function_id](lexeme)
                    if token is not None:
                        n = n - 1
                        if n == 0:
                            self.i = original_i
                            return token
                        else:
                            self.i = record[1]
                            break
                    else:
                        self.i = record[1]
                        break
