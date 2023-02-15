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

#
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
