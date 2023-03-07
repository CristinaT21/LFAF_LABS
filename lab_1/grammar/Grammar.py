import random as r
from lab_1.automaton.FiniteAutomaton import FiniteAutomaton


class Grammar(FiniteAutomaton):
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.string = self.S

    def generateWord(self):
        list_string = list(self.string)
        final = not any(x in list_string for x in self.VN)

        if final is False:
            for letter in self.string:
                if letter in self.VN:
                    self.string = self.string.replace(letter, self.P[letter][r.randint(0, len(self.P[letter]) - 1)])
                    return self.generateWord()
        else:
            return self.string

    def delete_string(self):
        self.string = self.S
        return self

    def toFiniteAutomaton(self):
        Q = set(self.VN + ['END'])
        Sigma = set(self.VT)
        delta = self.P_to_delta()
        q0 = 'S'
        F = {'END'}
        finite_automaton = FiniteAutomaton(Q=Q, Sigma=Sigma, delta=delta, q0=q0, F=F)
        return finite_automaton

    def P_to_delta(self):
        delta = {}

        for state, productions in self.P.items():
            transitions = {}
            for production in productions:
                if len(production) == 1:
                    transitions[production] = 'END'
                else:
                    transitions[production[0]] = production[1:]
            delta[state] = transitions
        delta['END'] = {'END': ''}
        return delta


    def classify_grammar(self):
        unrestricted = True
        context_sensitive = True
        context_free = True
        regular = True
        regular_left = True
        regular_right = True

        for state, productions in self.P.items():
            for production in productions:
                # check if the grammar exist
                for char in production:
                    if char not in self.VT + self.VN:
                        unrestricted, context_sensitive, context_free, regular, regular_left, regular_right = False
                        return f"The {char} does not belong to this grammar."

                for char in state:
                    if char not in self.VT + self.VN:
                        unrestricted, context_sensitive, context_free, regular, regular_left, regular_right = False
                        return f"The {char} is not in grammar"

                # check if type 1 or 0
                if (len(production) > 2 or len(state) > 1) and any([state_v in self.VN for state_v in state]):
                    context_free, regular, regular_left, regular_right = False

                # check type 1
                if any([ch in self.VN for ch in state]):
                    print("", end='')
                else:
                    context_sensitive, context_free, regular, regular_left, regular_right = False

                # type 2 or 3
                if len(production) <= 2 and len(state) == 1 and context_free:
                    if any([char_r in self.VN or len(char_r) == 0 for char_r in [production[1:]]]):
                        print("", end='')
                    else:
                        regular_right = False

                    if any([char_l in self.VN or len(char_l) == 0 for char_l in [production[0:1]]]):
                        print("", end='')
                    else:
                        regular_left = False

        if regular_left or regular_right:
            print(f"Regular(type 3)")
        elif context_free:
            print(f"Context-free(type 2)")
        elif context_sensitive:
            print(f"Context-sensitive(type 1)")
        elif unrestricted:
            print(f"Unrestricted(type 0)")
