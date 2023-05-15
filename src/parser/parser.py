from src.parser.parse_tree import ParseTree


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def remove_whitespace(self):
        for token in self.tokens:
            if token[1] == 'WHITESPACE':
                self.tokens.remove(token)
        
    def parse(self):
        self.remove_whitespace()
        if self.current_token()[1] == 'IF':
            return self.if_statement()
        elif self.current_token()[1] == 'WHILE':
            return self.while_statement()
        else:
            return self.math_expression()
        
    def if_statement(self):
        node = ParseTree('IF_STATEMENT')
        node.add_child(self.expect('IF'))
        node.add_child(self.expect('LPAREN'))
        node.add_child(self.expression())
        node.add_child(self.expect('RPAREN'))
        node.add_child(self.expect('LBRACE'))
        node.add_child(self.math_expression())
        node.add_child(self.expect('RBRACE'))
        if self.current_token_index < len(self.tokens) and self.current_token()[1] == 'ELSE':
            node.add_child(self.else_statement())
        node.add_child(self.expect('EOF'))
        return node

    def else_statement(self):
        node = ParseTree('ELSE_STATEMENT')
        node.add_child(self.expect('ELSE'))
        node.add_child(self.expect('LBRACE'))
        node.add_child(self.math_expression())
        node.add_child(self.expect('RBRACE'))
        return node

    def while_statement(self):
        node = ParseTree('WHILE_STATEMENT')
        node.add_child(self.expect('WHILE'))
        node.add_child(self.expect('LPAREN'))
        node.add_child(self.expression())
        node.add_child(self.expect('RPAREN'))
        node.add_child(self.expect('LBRACE'))
        node.add_child(self.math_expression())
        node.add_child(self.expect('RBRACE'))
        node.add_child(self.expect('EOF'))
        return node
    
    def math_expression(self):
        node = ParseTree('MATH_EXPRESSION')
        node.add_child(self.expect('IDENTIFIER'))
        node.add_child(self.expect('ASSIGN'))
        node.add_child(self.math_operation())

        return node
    
    def math_operation(self):
        node = ParseTree('MATH_OPERATION')
        if self.peek()[1] == 'SEMICOLON':
            if self.current_token()[1] == 'IDENTIFIER':
                node.add_child(self.expect('IDENTIFIER'))
                node.add_child(self.expect('SEMICOLON'))
            else:
                node.add_child(self.expect('NUMBER'))
                node.add_child(self.expect('SEMICOLON'))
        elif self.current_token()[1] != 'EOF':
            if self.current_token()[1] == 'IDENTIFIER':
                node.add_child(self.expect('IDENTIFIER'))
            else:
                node.add_child(self.expect('NUMBER'))
            if self.current_token()[1] == 'PLUS':
                node.add_child(self.expect('PLUS'))
            elif self.current_token()[1] == 'MINUS':
                node.add_child(self.expect('MINUS'))
            elif self.current_token()[1] == 'MULTIPLY':
                node.add_child(self.expect('MULTIPLY'))
            elif self.current_token()[1] == 'DIVIDE':
                node.add_child(self.expect('DIVIDE'))
            node.add_child(self.math_operation())
        elif self.current_token()[1] == 'EOF':
            node.add_child(self.expect('EOF'))
        return node
            
    def expression(self):
        node = ParseTree('EXPRESSION')
        node.add_child(self.expect('IDENTIFIER'))
        if self.current_token()[1] == 'EQUALS':
            node.add_child(self.expect('EQUALS'))
        elif self.current_token()[1] == 'NOTEQUALS':
            node.add_child(self.expect('NOTEQUALS'))
        elif self.current_token()[1] == 'LESSTHANOREQUALS':
            node.add_child(self.expect('LESSTHANOREQUALS'))
        elif self.current_token()[1] == 'GREATERTHANOREQUALS':
            node.add_child(self.expect('GREATERTHANOREQUALS'))
        elif self.current_token()[1] == 'LESSTHAN':
            node.add_child(self.expect('LESSTHAN'))
        elif self.current_token()[1] == 'GREATERTHAN':
            node.add_child(self.expect('GREATERTHAN'))
        if self.current_token()[1] == 'IDENTIFIER':
            node.add_child(self.expect('IDENTIFIER'))
        else:
            node.add_child(self.expect('NUMBER'))
        return node
        
    def expect(self, *expected_token_type):
        if self.current_token()[1] not in expected_token_type:
            raise RuntimeError(f'Error: expected {expected_token_type}, but got {self.current_token()[1]}, on position {self.current_token_index}.')
        node = ParseTree(self.current_token()[1], self.current_token()[0])
        self.advance()
        return node
        
    def current_token(self):
        return self.tokens[self.current_token_index]
    
    def peek(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        else:
            return '', ''
        
    def advance(self):
        self.current_token_index += 1
