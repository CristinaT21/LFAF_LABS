# Lab no. 5

### Course: Formal Languages & Finite Automata
### Author: Cristina Țărnă

----
## Short description:
Parsing, or the act of gathering syntactical meaning or conducting a syntactical analysis of text, can be alternatively referred to as the process of collecting and structuring information. This process typically yields a parse tree that may include semantic details, which can be utilized in later stages of compilation.
## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed.
2. Get familiar with the concept of AST.
3. In addition to what has been done in the 3rd lab work do the following:
   - In case you didn't have a type that denotes the possible types of tokens you need to:
     * Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.
     * Please use regular expressions to identify the type of the token.
   - Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   - Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description

The *Parser* class that is responsible for parsing a sequence of tokens.
It has methods for removing whitespace, parsing different types of statements 
(if, else, while), parsing mathematical expressions, and handling token 
expectations. The parsing process involves constructing a parse tree using 
the provided tokens. The class keeps track of the current token index and 
provides methods to advance to the next token and peek at the next token 
without consuming it. The class also utilizes another class called 
"ParseTree" to represent the parse tree structure.

#### The remove whitespace function
```python
def remove_whitespace(self):
    for token in self.tokens:
        if token[1] == 'WHITESPACE':
            self.tokens.remove(token)
```
This function removes all whitespace tokens from the token list to parse easier.
#### The parse function
```python
def parse(self):
    self.remove_whitespace()
    if self.current_token()[1] == 'IF':
        return self.if_statement()
    elif self.current_token()[1] == 'WHILE':
        return self.while_statement()
    else:
        return self.math_expression()
```
Here we can have just 3 starting points(an if statement, a while statement or a math expression.)
#### The if statement function
```python   
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
```
I add the children to the node and return it.
IF -> LPAREN -> EXPRESSION -> RPAREN -> LBRACE -> MATH_EXPRESSION -> RBRACE -> EOF
Here, we have an if statement that can have an else statement or not. 
expression() is a function that returns a node with the expression made for 
the comparator part.
math_expression() is a function that returns a node with the expression made for
assigning a value to a variable kind of expressions.
#### The else statement function
```python
def else_statement(self):
    node = ParseTree('ELSE_STATEMENT')
    node.add_child(self.expect('ELSE'))
    node.add_child(self.expect('LBRACE'))
    node.add_child(self.math_expression())
    node.add_child(self.expect('RBRACE'))
    return node
```
It parses the else statement.
I add a node 'ELSE_STATEMENT' in the tree and add the children to it.
ELSE -> LBRACE -> MATH_EXPRESSION -> RBRACE

#### The while statement function
```python   
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
```
Here, we have a while statement that can have an expression and a math expression.
I add a node 'WHILE_STATEMENT' in the tree and add the children to it.

WHILE -> LPAREN -> EXPRESSION -> RPAREN -> LBRACE -> MATH_EXPRESSION -> RBRACE -> EOF

#### The math expression function
```python
def math_expression(self):
    node = ParseTree('MATH_EXPRESSION')
    node.add_child(self.expect('IDENTIFIER'))
    node.add_child(self.expect('ASSIGN'))
    node.add_child(self.math_operation())

    return node
```
In this function, I add a node 'MATH_EXPRESSION' in the tree and add the children to it.
IDENTIFIER -> ASSIGN -> MATH_OPERATION

#### The math operation function
```python
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
```
Here, I add a node 'MATH_OPERATION' in the tree and add the children to it.
I check if the next token is a semicolon, if it is, I add the identifier or the number and the semicolon.
If it is not, I add the identifier or the number and the operator and then I call the function again.
If the current token is EOF, I add the EOF token to the tree.
Then I return the node.

#### The expression function
```python   
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
```
Here, I add a node 'EXPRESSION' in the tree and add the children to it.
I check if the next token is an operator, if it is, I add the identifier or the number and the operator.
Then I return the node.

#### The expect function
```python
def expect(self, *expected_token_type):
    if self.current_token()[1] not in expected_token_type:
        raise RuntimeError(f'Error: expected {expected_token_type}, but got {self.current_token()[1]}, on position {self.current_token_index}.')
    node = ParseTree(self.current_token()[1], self.current_token()[0])
    self.advance()
    return node
```
Here, I check if the current token is the expected token type, if it is not, I raise an error.
If it is, I add a node with the token type and the token text and then I advance.

#### The advance function
```python
def advance(self):
    self.current_token_index += 1
```
Here, I increment the current token index.

#### The current token function
```python
def current_token(self):
    return self.tokens[self.current_token_index]
```
Here, I return the current token.

#### The peek function
```python
def peek(self):
    return self.tokens[self.current_token_index + 1]
```
Here, I return the next token. I use this function to check if the next token is a semicolon.
#### The print tree function
```python
def print_tree(self, level=0):
    result = "\t" * level + f"{self.token_type}"
    if self.text:
        result += f": {self.text}"
    result += "\n"
    for child in self.children:
        result += child.print_tree(level + 1)
    return result
```
This function prints the tree in a readable format - AST.

### Code snippets from Main class:

```
expression = input("Enter expression to be tokenized and parsed: ")
tokens = Lexer().tokenize(expression)
print(tokens)
print('Your expression parsed:')
parser = Parser(tokens).parse()
print(parser.print_tree())    
```
Here, I ask the user to enter an expression, then I tokenize it and print the tokens.
Then I parse the expression and print the AST.

## Results:
Enter expression to be tokenized and parsed: if ( x == 5 ) { y = 2 * x * z; } else { y = x / 2; }
```
[('if', 'IF'), (' ', 'WHITESPACE'), ('(', 'LPAREN'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('==', 'EQUALS'), (' ', 'WHITESPACE'), ('5', 'NUMBER'), (' ', 'WHITESPACE'), (')', 'RPAREN'), (' ', 'WHITESPACE'), ('{', 'LBRACE'), (' ', 'WHITESPACE'), ('y', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('2', 'NUMBER'), (' ', 'WHITESPACE'), ('*', 'MULTIPLY'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('*', 'MULTIPLY'), (' ', 'WHITESPACE'), ('z', 'IDENTIFIER'), (';', 'SEMICOLON'), (' ', 'WHITESPACE'), ('}', 'RBRACE'), (' ', 'WHITESPACE'), ('else', 'ELSE'), (' ', 'WHITESPACE'), ('{', 'LBRACE'), (' ', 'WHITESPACE'), ('y', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('/', 'DIVIDE'), (' ', 'WHITESPACE'), ('2', 'NUMBER'), (';', 'SEMICOLON'), (' ', 'WHITESPACE'), ('}', 'RBRACE'), (' ', 'EOF')]

Your expression parsed:
IF_STATEMENT
	IF: if
	LPAREN: (
	EXPRESSION
		IDENTIFIER: x
		EQUALS: ==
		NUMBER: 5
	RPAREN: )
	LBRACE: {
	MATH_EXPRESSION
		IDENTIFIER: y
		ASSIGN: =
		MATH_OPERATION
			NUMBER: 2
			MULTIPLY: *
			MATH_OPERATION
				IDENTIFIER: x
				MULTIPLY: *
				MATH_OPERATION
					IDENTIFIER: z
					SEMICOLON: ;
	RBRACE: }
	ELSE_STATEMENT
		ELSE: else
		LBRACE: {
		MATH_EXPRESSION
			IDENTIFIER: y
			ASSIGN: =
			MATH_OPERATION
				IDENTIFIER: x
				DIVIDE: /
				MATH_OPERATION
					NUMBER: 2
					SEMICOLON: ;
		RBRACE: }
	EOF:
```