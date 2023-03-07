from lab_1.grammar.Grammar import Grammar
from lab_1.automaton.FiniteAutomaton import FiniteAutomaton
import graphviz

# Define the grammar
VN = ["S", "A", "B", "C"]
VT = ["a", "b", "c", "d"]
P = {
    "S": ["dA"],
    "A": ["aB", "b"],
    "B": ["bC", "d"],
    "C": ["cB", "aA"]
}
string_list = []

#define the finite automaton
Q = {'q0', 'q1', 'q2', 'q3'}
Sigma = {'a', 'b', 'c'}
q0 = 'q0'
F = {'q3'}
delta = dict(q0={'a': 'q1', 'b': 'q0'},
             q1={'a': 'q2', 'b': 'q1'},
             q2={'c': 'q3'},
             q3={'c': 'q3'})

nfa = FiniteAutomaton(Q, Sigma, delta, q0, F)

if __name__ == '__main__':
    grammar: Grammar = Grammar(VN=VN, VT=VT, P=P, S='S')

    while len(string_list) < 6:
        string = grammar.generateWord()
        if string not in string_list:
            grammar.delete_string()
            string_list.append(string)
        else:
            grammar.delete_string()
            continue

    print('5 valid strings:')
    print(string_list)

    print(grammar.classify_grammar())

    finite_automaton: FiniteAutomaton = FiniteAutomaton(Q=Q, Sigma=Sigma, delta=delta, q0=q0, F=F)
    gr = finite_automaton.to_regular_grammar()
    print(f'Start is {gr.S}, terminals are {gr.VT}, non-terminals are {gr.VN}, the production is {gr.P}')
    fa = grammar.toFiniteAutomaton()
    print(f'Start is {fa.q0}, the states are {fa.Q}, the alphabet is {fa.Sigma}, the transitions are {fa.delta}, the final state is {fa.F}')

    finite_automaton.nfa_to_dfa()


    for i in range(2):
        word: str = input('Enter a word to check if it corresponds to the grammar rules: ')
        print(fa.stringBelongToLanguage(word))
