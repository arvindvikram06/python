from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

# Sample source code
code = """
x = 0
while (x < 5) {
    x = x + 1
}
"""

# 1. Lexical Analysis: Convert text to tokens
tokens = tokenize(code)

# 2. Syntactic Analysis: Convert tokens to an AST
parser = Parser(tokens)
ast = parser.parse()

# 3. Execution: Run the AST using the Interpreter
interpreter = Interpreter()
interpreter.eval(ast)

# Display final results
print("Final Environment:", interpreter.env)
print("Value of x:", interpreter.env["x"])