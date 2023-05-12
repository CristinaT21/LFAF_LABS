# Lab no. 3

### Course: Formal Languages & Finite Automata
### Author: Cristina Țărnă

----
## Short description:
The term lexer represents the process of extracting lexical tokens from a string of characters.
The lexeme is just the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each lexeme.
## Objectives:
* Understand what lexical analysis is.

* Get familiar with the inner workings of a lexer/scanner/tokenizer.

* Implement a sample lexer and show how it works.

## Implementation description

In the Lexer class, I defined a dictionary of regular expressions that will be used to tokenize the input string.
An example of some tokens:
```
      r'\bif\b': 'IF',
      r'\belse\b': 'ELSE'
      r'\bwhile\b': 'WHILE'
  }
```
#### The tokenizing function
```
def tokenize(self, input_string):
  # Set the input string
  self.input_string = input_string
  # Initialize an empty list to hold the tokens
  self.tokens_list = []
  while self.input_string:
      # Initialize a variable to hold the current match
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
```
#### Let's dive deeper.
#### The function takes a string to be tokenized
```
def tokenize(self, input_string):
```
#### Loop until string is empty
```
  while self.input_string:
```

#### Loop through the token patterns
```
    for pattern, token_type in self.tokens.items():
     # Compile the pattern as a regular expression
            regex = re.compile(pattern)
            # Try to match the pattern to the input string
            match = regex.match(self.input_string)
            # If there's a match, create a token and add it to the list
            if match:
                text = match.group(0)
                self.tokens_list.append((text, token_type))
                self.input_string = self.input_string[len(text):]
                break
```
1. For each iteration of the loop, loop through the token patterns using a **for** 
loop that iterates over the **self.tokens** dictionary.
2. For each pattern, compile it into a regular expression using the **re.compile()** function.
3. Try to match the pattern to the input string using the **regex.match()** method. If there's a match, 
create a token and add it to the list of tokens.

```
            if not match:
                raise ValueError(f'Invalid character: {self.input_string[0]}')
```
If there's no match, raise a **ValueError** with a message indicating the first invalid character in the input string.

```
return self.tokens_list
```
Return the list of tokens.

### Code snippets from Main class:

```
expression = input("Enter expression to be tokenizer ")
print('Your expression tokenized:')
print(Lexer().tokenize(expression))      
```
Here, a string inputted by the user will be tokenized. 
A *Lexer* object is created using **Lexer()**, then the method **tokenize()** is applied 
on the *expression* inputted by the user. 
The **tokenize()** method breaks the input string down into a list of individual tokens using the regular expressions defined in the tokens dictionary, and returns the resulting list of tuples.
Finally, **print(Lexer().tokenize(expression))** prints the resulting list of tokens to the console.

## Results:
Enter expression to be tokenizer x = y * 2;


Your expression tokenized:

[('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('y', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('*', 'MULTIPLY'), (' ', 'WHITESPACE'), ('2', 'NUMBER'), (';', 'SEMICOLON')]

First expression: if (x <= 5) { y = x * 2; } else { y = x / 2; }

[('if', 'IF'), (' ', 'WHITESPACE'), ('(', 'LPAREN'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('<', 'LESSTHAN'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('5', 'NUMBER'), (')', 'RPAREN'), (' ', 'WHITESPACE'), ('{', 'LBRACE'), (' ', 'WHITESPACE'), ('y', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('*', 'MULTIPLY'), (' ', 'WHITESPACE'), ('2', 'NUMBER'), (';', 'SEMICOLON'), (' ', 'WHITESPACE'), ('}', 'RBRACE'), (' ', 'WHITESPACE'), ('else', 'ELSE'), (' ', 'WHITESPACE'), ('{', 'LBRACE'), (' ', 'WHITESPACE'), ('y', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('/', 'DIVIDE'), (' ', 'WHITESPACE'), ('2', 'NUMBER'), (';', 'SEMICOLON'), (' ', 'WHITESPACE'), ('}', 'RBRACE')]


Second expression: while (x > 0) { x = x - 1; }:

[('while', 'WHILE'), (' ', 'WHITESPACE'), ('(', 'LPAREN'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('>', 'GREATERTHAN'), (' ', 'WHITESPACE'), ('0', 'NUMBER'), (')', 'RPAREN'), (' ', 'WHITESPACE'), ('{', 'LBRACE'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('x', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('-', 'MINUS'), (' ', 'WHITESPACE'), ('1', 'NUMBER'), (';', 'SEMICOLON'), (' ', 'WHITESPACE'), ('}', 'RBRACE')]

Third expression: z = (true and false) or not true;:

[('z', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('(', 'LPAREN'), ('true', 'TRUE'), (' ', 'WHITESPACE'), ('and', 'AND'), (' ', 'WHITESPACE'), ('false', 'FALSE'), (')', 'RPAREN'), (' ', 'WHITESPACE'), ('or', 'OR'), (' ', 'WHITESPACE'), ('not', 'NOT'), (' ', 'WHITESPACE'), ('true', 'TRUE'), (';', 'SEMICOLON')]

Forth expression: a != b;:

[('a', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('!=', 'NOTEQUALS'), (' ', 'WHITESPACE'), ('b', 'IDENTIFIER'), (';', 'SEMICOLON')]

Fifth expression: you = cool;:

[('you', 'IDENTIFIER'), (' ', 'WHITESPACE'), ('=', 'ASSIGN'), (' ', 'WHITESPACE'), ('cool', 'IDENTIFIER'), (';', 'SEMICOLON')]

