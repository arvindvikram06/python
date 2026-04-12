from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.depth = 0

    def log(self, msg):
        print("  " * self.depth + msg)

    def peek(self):
        return self.tokens[self.pos]

    def eat(self, type_):
        token = self.peek()
        if token[0] == type_:
            self.log(f"Eat {token}")
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token}")

    def parse_factor(self):
        token = self.peek()
        self.log(f"parse_factor {token}")

        if token[0] == "NUMBER":
            return Number(self.eat("NUMBER")[1])

        elif token[0] == "IDENT":
            return Var(self.eat("IDENT")[1])

        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            self.depth += 1
            expr = self.parse_comparison()
            self.depth -= 1
            self.eat("RPAREN")
            return expr

    def parse_term(self):
        self.log("parse_term")
        self.depth += 1

        node = self.parse_factor()

        while self.peek()[0] in ("MUL", "DIV"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_factor()
            node = BinOp(node, op, right)

        self.depth -= 1
        return node

    def parse_expr(self):
        self.log("parse_expr")
        self.depth += 1

        node = self.parse_term()

        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_term()
            node = BinOp(node, op, right)

        self.depth -= 1
        return node

    def parse_comparison(self):
        self.log("parse_comparison")
        self.depth += 1

        node = self.parse_expr()

        if self.peek()[0] in ("LT","GT","LE","GE","EQ","NE"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_expr()
            node = BinOp(node, op, right)

        self.depth -= 1
        return node

    def parse_assign(self):
        self.log("parse_assign")
        self.depth += 1

        name = self.eat("IDENT")[1]
        self.eat("EQUAL")
        value = self.parse_comparison()

        self.depth -= 1
        return Assign(name, value)

    def parse_block(self):
        self.log("parse_block")
        self.depth += 1

        self.eat("LBRACE")
        stmts = []

        while self.peek()[0] != "RBRACE":
            stmts.append(self.parse_statement())

        self.eat("RBRACE")

        self.depth -= 1
        return Block(stmts)

    def parse_if(self):
        self.log("parse_if")
        self.depth += 1

        self.eat("IF")
        self.eat("LPAREN")
        cond = self.parse_comparison()
        self.eat("RPAREN")

        then_branch = self.parse_block()

        else_branch = None
        if self.peek()[0] == "ELSE":
            self.eat("ELSE")
            else_branch = self.parse_block()

        self.depth -= 1
        return If(cond, then_branch, else_branch)

    def parse_statement(self):
        token = self.peek()

        if token[0] == "IF":
            return self.parse_if()

        elif token[0] == "WHILE":
            return self.parse_while()

        elif token[0] == "IDENT" and self.tokens[self.pos+1][0] == "EQUAL":
            return self.parse_assign()

        else:
            return self.parse_expr()

    def parse_while(self):
        self.log("parse_while")
        self.depth += 1

        self.eat("WHILE")
        self.eat("LPAREN")
        cond = self.parse_comparison()
        self.eat("RPAREN")

        body = self.parse_block()

        self.depth -= 1
        return While(cond, body)

    def parse(self):
        self.log("parse program")
        statements = []

        while self.peek()[0] != "EOF":
            statements.append(self.parse_statement())

        return Block(statements)