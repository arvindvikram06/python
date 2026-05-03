from ast_nodes import *

# Recursive descent parser that builds an AST from tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # Look at the current token without consuming it
    def peek(self):
        return self.tokens[self.pos]

    # Verify and consume the expected token type
    def eat(self, type_):
        token = self.peek()
        if token[0] == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token}")

    # Handles numbers, variables, and parenthesized expressions
    def parse_factor(self):
        token = self.peek()
        if token[0] == "NUMBER":
            return Number(self.eat("NUMBER")[1])
        elif token[0] == "IDENT":
            return Var(self.eat("IDENT")[1])
        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_comparison()
            self.eat("RPAREN")
            return expr

    # Handles multiplication and division (high precedence)
    def parse_term(self):
        node = self.parse_factor()
        while self.peek()[0] in ("MUL", "DIV"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_factor()
            node = BinOp(node, op, right)
        return node

    # Handles addition and subtraction (medium precedence)
    def parse_expr(self):
        node = self.parse_term()
        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_term()
            node = BinOp(node, op, right)
        return node

    # Handles comparisons like <, >, == (low precedence)
    def parse_comparison(self):
        node = self.parse_expr()
        if self.peek()[0] in ("LT", "GT", "LE", "GE", "EQ", "NE"):
            op = self.eat(self.peek()[0])[1]
            right = self.parse_expr()
            node = BinOp(node, op, right)
        return node

    # Handles variable assignments (x = 5)
    def parse_assign(self):
        name = self.eat("IDENT")[1]
        self.eat("EQUAL")
        value = self.parse_comparison()
        return Assign(name, value)

    # Handles blocks of code inside braces {}
    def parse_block(self):
        self.eat("LBRACE")
        stmts = []
        while self.peek()[0] != "RBRACE":
            stmts.append(self.parse_statement())
        self.eat("RBRACE")
        return Block(stmts)

    # Handles If-Else control flow
    def parse_if(self):
        self.eat("IF")
        self.eat("LPAREN")
        cond = self.parse_comparison()
        self.eat("RPAREN")
        then_branch = self.parse_block()
        else_branch = None
        if self.peek()[0] == "ELSE":
            self.eat("ELSE")
            else_branch = self.parse_block()
        return If(cond, then_branch, else_branch)

    # Routes to specific statement types (if, while, assign, etc.)
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

    # Handles While loops
    def parse_while(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        cond = self.parse_comparison()
        self.eat("RPAREN")
        body = self.parse_block()
        return While(cond, body)

    # Main entry point: parses the full program into a Block
    def parse(self):
        statements = []
        while self.peek()[0] != "EOF":
            statements.append(self.parse_statement())
        return Block(statements)