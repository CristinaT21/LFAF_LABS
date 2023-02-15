from lab_1.grammar.Grammar import Grammar

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

    fa = grammar.toFiniteAutomaton()
    for i in range(2):
        word: str = input('Enter a word to check if it corresponds to the grammar rules: ')
        print(fa.stringBelongToLanguage(word))
