from src.grammar.Grammar import Grammar
from src.automaton.FiniteAutomaton import FiniteAutomaton
from automathon import DFA
from PIL import Image
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

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
        # src
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
        # src
        fa = grammar.toFiniteAutomaton()
        print('\nFrom grammar to finite automaton')
        print(f'Start is {fa.q0},\n the states are {fa.Q},\n the alphabet is {fa.Sigma},\n'
              f' the transitions are {fa.delta},\n the final state is {fa.F}')
        print('\nFinite Automaton is deterministic: ')
        # src
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

        print(f'First expression: {expression1}')
        print(Lexer().tokenize(expression1))
        print(f'\nSecond expression: {expression2}:')
        print(Lexer().tokenize(expression2))
        print(f'\nThird expression: {expression3}:')
        print(Lexer().tokenize(expression3))
        print(f'\nForth expression: {expression4}:')
        print(Lexer().tokenize(expression4))
        print(f'\nFifth expression: {expression5}:')
        print(Lexer().tokenize(expression5))

    elif lab_no == 4:
        # lab 4
        # To Chomsky Normal Form
        P1 = {
            "S": ["aBA", "AB"],
            "A": ["d", "dS", "AbBA", "epsilon"],
            "B": ["a", "aS", "A"],
            "D": ["Aba"]
        }
        g: Grammar = Grammar(VN=["S", "A", "B", "D"], VT=["a", "b", "d"], P=P1, S='S')
        opt_no = int(input("Enter 1 to see the final result or 2 to see each step: "))
        if opt_no == 1:
            print('\nGrammar in Chomsky Normal Form:')
            g.toChomskyNormalForm()
            print(g.P)
        elif opt_no == 2:
            print('See each step:')
            g.eliminateEpsilonProductions()
            print("Eliminate Epsilon Productions", g.P)
            g.eliminateUnitProductions()
            print("Eliminate Unit Productions", g.P)
            g.eliminateInaccessibleSymbols()
            print('Eliminate Inaccessible Symbols', g.P)
            g.eliminateNonproductiveSymbols()
            print('Eliminate Nonproductive Symbols', g.P)
            g.eliminateLongProductions()
            print('Eliminate Long Productions', g.P)
    elif lab_no == 5:
        # lab 3
        expression = input("Enter expression to be tokenized and parsed: ")
        # example: 'if (x < 10) { y = x * 5; }'
        tokens = Lexer().tokenize(expression)
        print(tokens)
        print('Your expression parsed:')
        parser = Parser(tokens).parse()
        print(parser.print_tree())

    else:
        print("Try the number 1 up to 4.")
