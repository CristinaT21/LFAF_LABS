import re


class Lexer:
    def __init__(self) -> object:
        self.input_string = None
        self.tokens_list = None
        self.tokens = {
            r'\bif\b': 'IF',
            r'\belse\b': 'ELSE',
            r'\bwhile\b': 'WHILE',
            r'\btrue\b': 'TRUE',
            r'\bfalse\b': 'FALSE',
            r'\bnot\b': 'NOT',
            r'\bor\b': 'OR',
            r'\band\b': 'AND',
            r'\(': 'LPAREN',
            r'\)': 'RPAREN',
            r'\{': 'LBRACE',
            r'\}': 'RBRACE',
            r';': 'SEMICOLON',
            r'\+': 'PLUS',
            r'-': 'MINUS',
            r'\*': 'MULTIPLY',
            r'/': 'DIVIDE',
            r'\*\*': 'POWER',
            r'=': 'ASSIGN',
            r'==': 'EQUALS',
            r'!=': 'NOTEQUALS',
            r'<': 'LESSTHAN',
            r'>': 'GREATERTHAN',
            r'<=': 'LESSTHANOREQUALS',
            r'>=': 'GREATERTHANOREQUALS',
            r'\d+(\.\d+)?': 'NUMBER',
            r'[a-zA-Z_]\w*': 'IDENTIFIER',
            r'\s+': 'WHITESPACE'
        }

    def tokenize(self, input_string):
        self.input_string = input_string
        self.tokens_list = []
        while self.input_string:
            match = None
            for pattern, token_type in self.tokens.items():
                regex = re.compile(pattern)
                match = regex.match(self.input_string)
                if match:
                    text = match.group(0)
                    self.tokens_list.append((text, token_type))
                    self.input_string = self.input_string[len(text):]
                    break
            if not match:
                raise ValueError(f'Invalid character: {self.input_string[0]}')
        return self.tokens_list
