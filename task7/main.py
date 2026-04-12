from lexer import tokenize
from parser import Parser

code = "x = 10 + 5 * 2"

tokens = tokenize(code)
print("TOKENS:", tokens)

parser = Parser(tokens)
ast = parser.parse()

print("AST:", ast)