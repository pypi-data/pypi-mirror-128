class _NFA:
    pass


class NFA(_NFA):
    STATE_ID = -1

    def __init__(self, final_states=None, name=""):
        if final_states is None:
            final_states = set()
        NFA.STATE_ID += 1

        self.id = NFA.STATE_ID
        self.final_states = final_states
        self.transitions = {}
        self.name = f"STATE: {self.id}" if name == "" else name

    def add_transition(self, state: _NFA, symbol: str):
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

    def subset_construction(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)

        if "EPSILON" in self.transitions:
            epsilon_transitions = self.transitions["EPSILON"].copy()
            epsilon_visited = set()
            while len(epsilon_transitions) > 0:
                epsilon_state = epsilon_transitions.pop()
                if epsilon_state not in epsilon_visited:
                    epsilon_visited.add(epsilon_state)
                    if "EPSILON" in epsilon_state.transitions:
                        epsilon_transitions = epsilon_transitions.union(
                            epsilon_state.transitions["EPSILON"]
                        )
                    for key in epsilon_state.transitions.keys():
                        for state in epsilon_state.transitions[key]:
                            self.add_transition(state, key)

        for symbol, states in self.transitions.items():
            for state in states:
                state.subset_construction(visited)

    def is_final_state(self, final_states):
        if self in final_states:
            return self
        for state in final_states:
            if "EPSILON" in self.transitions and state in self.transitions["EPSILON"]:
                return state
        return False

    def delta(self, symbol):
        transitions = set()
        if symbol in self.transitions:
            transitions = self.transitions[symbol]
        return transitions

    def __str__(self):
        return self.name + f"({len(self.transitions)})"

    def __repr__(self):
        return str(self)

    def display(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for symbol in self.transitions:
            for state in self.transitions[symbol]:
                print(f"{self} -- {symbol} --> {state}")

        for symbol in self.transitions:
            for state in self.transitions[symbol]:
                state.display(visited)


def _combine_nfas(nfas: list):
    initial_state = NFA()
    for nfa in nfas:
        initial_state.add_transition(nfa, "EPSILON")
        initial_state.final_states = initial_state.final_states.union(nfa.final_states)
    return initial_state
