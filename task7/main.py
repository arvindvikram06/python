from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

code = """
x = 0

while (x < 5) {
    x = x + 1
}
"""

tokens = tokenize(code)
print("TOKENS:", tokens)

parser = Parser(tokens)
ast = parser.parse()

print("\n--- INTERPRETER ---\n")

interpreter = Interpreter()
interpreter.eval(ast)

print("\nFinal ENV:", interpreter.env)

print("Output",interpreter.env["x"])