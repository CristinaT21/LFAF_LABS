

class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def stringBelongToLanguage(self, word: str):
        q = self.q0
        for c in word:
            if c not in self.Sigma:
                return False
            q = self.delta[q].get(c)
            if q is None:
                return False
        return q in self.F

    def to_regular_grammar(self):
        from lab_1.grammar.Grammar import Grammar

        V = set(self.Q)  # set of variables
        VN = {f"A{i}" for i in range(len(self.Q))}  # set of variables for the regular grammar
        VT = set(self.Sigma)  # set of terminals
        S = self.q0  # start variable
        S_prime = "S'"  # start variable for the regular grammar
        P = set()  # set of rules

        # create rules for transitions
        for state in self.Q:
            for symbol in self.Sigma:
                if (state, symbol) in self.delta:
                    next_state = self.delta[(state, symbol)]
                    rule = f"{state} -> {symbol}{next_state}"
                    P.add(rule)

        # create rules for accepting states
        for state in self.F:
            rule = f"{state} -> epsilon"
            P.add(rule)

        # create the start rule
        start_rule = f"{S_prime} -> {S}"
        P.add(start_rule)

        return Grammar(VN, VT, P, S_prime)

    def nfa_to_dfa(self):
        alphabet = set()
        for transitions in self.delta.values():
            alphabet.update(transitions.keys())

        start_state = self.q0
        dfa_states = [set([start_state])]
        dfa_transitions = {}
        unmarked_states = [0]

        while unmarked_states:
            index = unmarked_states.pop()
            current_state = dfa_states[index]

            for symbol in alphabet:
                next_state = set()
                for nfa_state in current_state:
                    if nfa_state in self.q0:
                        if symbol in self[nfa_state]:
                            next_nfa_states = self[nfa_state][symbol]
                        else:
                            next_nfa_states = set()
                    else:
                        next_nfa_states = set()
                    next_state.update(next_nfa_states)

                if next_state:
                    next_state = set(next_state)
                    if next_state not in dfa_states:
                        dfa_states.append(next_state)
                        unmarked_states.append(len(dfa_states) - 1)

                    current_symbol_transitions = dfa_transitions.get(index, {})
                    current_symbol_transitions[symbol] = dfa_states.index(next_state)
                    dfa_transitions[index] = current_symbol_transitions

        dfa_final_states = set()
        for i, state in enumerate(dfa_states):
            if state.intersection(self.F):
                dfa_final_states.add(i)

        return dfa_states, alphabet, dfa_transitions, 0, dfa_final_states


# # Define the finite automaton
# Q = {'S', 'A', 'B', 'C', 'END'}
# Sigma = {'a', 'b', 'c', 'd'}
# delta = {
#     'S': {'d': 'A'},
#     'A': {'a': 'B', 'b': 'END'},
#     'B': {'b': 'C', 'd': 'END'},
#     'C': {'c': 'B', 'a': 'A'},
#     'END': {}
# }
# q0 = 'S'
# F = {'END'}
