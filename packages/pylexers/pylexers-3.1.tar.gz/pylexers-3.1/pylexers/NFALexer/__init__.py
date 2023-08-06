from pylexers.BaseLexer import Lexer
from pylexers.NFALexer.NFA import NFA, _combine_nfas
from pylexers.NFALexer.nfa_from_re import _regular_expression_to_nfa


class NFALexer(Lexer):
    def __init__(self, regular_expressions: list, tokenize_functions: list):
        super().__init__(regular_expressions, tokenize_functions)
        nfa_list = [_regular_expression_to_nfa(re) for re in regular_expressions]
        self.tokenize_functions = dict()
        for i in range(len(nfa_list)):
            for accepting_state in nfa_list[i].final_states:
                self.tokenize_functions[accepting_state] = tokenize_functions[i]

        self.initial_state = _combine_nfas(nfa_list)
        self.final_states = self.initial_state.final_states
        self.initial_state.subset_construction()
        self.source_program = ""

    def get_successful_id(self, states):
        for state in states:
            if state.is_final_state(self.final_states):
                return state.is_final_state(self.final_states)
        return False

    def is_failure_state(self, states):
        if states == set():
            return True
        return False

    def find_records(self):
        i = self.i
        j = self.i
        records = []
        states = {self.initial_state}
        while len(self.source_program) > j:
            next_states = set()
            for state in states:
                next_states = next_states.union(state.delta(self.source_program[j]))
            states = next_states
            j += 1
            records += [(i, j, states)]
            if self.is_failure_state(states):
                break
        return records
