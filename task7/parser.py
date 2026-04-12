from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def eat(self, type_):
        token = self.peek()
        if token[0] == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token}")

    def parse_factor(self):
        token = self.peek()

        if token[0] == "NUMBER":
            return Number(self.eat("NUMBER")[1])

        elif token[0] == "IDENT":
            return Var(self.eat("IDENT")[1])

        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_expr()
            self.eat("RPAREN")
            return expr

    def parse_term(self):
        node = self.parse_factor()

        while self.peek()[0] in ("MUL", "DIV"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_factor()
            node = BinOp(node, op, right)

        return node

    def parse_expr(self):
        node = self.parse_term()

        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_term()
            node = BinOp(node, op, right)

        return node

    def parse_assign(self):
        name = self.eat("IDENT")[1]
        self.eat("EQUAL")
        value = self.parse_expr()
        return Assign(name, value)

    def parse(self):
        return self.parse_assign()