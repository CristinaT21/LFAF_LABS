from lab_1.grammar.Grammar import Grammar
from lab_1.automaton.FiniteAutomaton import FiniteAutomaton
from automathon import DFA
from PIL import Image
from lab_1.lexer.lexer import Lexer

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

# define the finite automaton
Q = {'q0', 'q1', 'q2', 'q3'}
Sigma = {'a', 'b', 'c'}
q0 = 'q0'
F = {'q3'}
delta = dict(q0={'a': 'q1', 'b': 'q0'},
             q1={'a': 'q2', 'b': 'q1'},
             q2={'c': 'q3'},
             q3={'c': 'q3'})


if __name__ == '__main__':
    lab_no = int(input("Enter the lab you want to run: "))
    if lab_no == 1:
        grammar: Grammar = Grammar(VN=VN, VT=VT, P=P, S='S')
        # lab_1
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
        # lab_1
        fa = grammar.toFiniteAutomaton()
        print('\nFrom grammar to finite automaton')
        print(f'Start is {fa.q0},\n the states are {fa.Q},\n the alphabet is {fa.Sigma},\n'
              f' the transitions are {fa.delta},\n the final state is {fa.F}')
        print('\nFinite Automaton is deterministic: ')
        # lab_1
        for i in range(2):
            word: str = input('Enter a word to check if it corresponds to the grammar rules: ')
            print(fa.stringBelongToLanguage(word))
    elif lab_no == 2:
        # lab_2
        grammar: Grammar = Grammar(VN=VN, VT=VT, P=P, S='S')
        print('\nGrammar type:')
        print(grammar.classify_grammar())
        # lab_2
        finite_automaton: FiniteAutomaton = FiniteAutomaton(Q=Q, Sigma=Sigma, delta=delta, q0=q0, F=F)
        gr = finite_automaton.to_regular_grammar()
        print('\nFrom finite automaton to regular grammar:')
        print(f'Start is {gr.S},\n terminals are {gr.VT},\n non-terminals are {gr.VN},\n'
              f' the production is {gr.P}')
        # lab_2
        print(finite_automaton.is_deterministic())
        print('\nFrom NFA to DFA:')
        print(finite_automaton.nfa_to_dfa())
        print('\n')
        # lab_2
        automathon_1 = DFA(Q, Sigma, delta, q0, F)
        automathon_1.view('visualization')
        image = Image.open('visualization.gv.png')
        image.show()
    elif lab_no == 3:
        # lab 3
        expression = input("Enter expression to be tokenizer ")
        # example: 'if (x < 10) { y = x * 5; }'
        print('Your expression tokenized:')
        print(Lexer().tokenize(expression))
        expression1 = 'if (x <= 5) { y = x * 2; } else { y = x / 2; }'
        expression2 = 'while (x > 0) { x = x - 1; }'
        expression3 = 'z = (true and false) or not true;'
        expression4 = 'a != b;'
        expression5 = 'you = cool;'

        print('First:')
        print(Lexer().tokenize(expression1))
        print('\nSecond:')
        print(Lexer().tokenize(expression2))
        print('\nThird:')
        print(Lexer().tokenize(expression3))
        print('\nForth:')
        print(Lexer().tokenize(expression4))
        print('\nFifth:')
        print(Lexer().tokenize(expression5))

    else:
        print("Try the number 1 up to 3.")
