from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.env = {}
        self.depth = 0

    def log(self, msg):
        print("  " * self.depth + msg)

    def eval(self, node):
        if isinstance(node, Number):
            self.log(f"Number -> {node.value}")
            return node.value

        elif isinstance(node, Var):
            self.log(f"Var -> {node.name}")
            return self.env[node.name]

        elif isinstance(node, Assign):
            self.log(f"Assign -> {node.name}")
            self.depth += 1

            value = self.eval(node.value)
            self.env[node.name] = value

            self.depth -= 1
            self.log(f"Stored {node.name} = {value}")
            return value

        elif isinstance(node, BinOp):
            self.log(f"BinOp -> {node.op}")
            self.depth += 1

            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == '+': result = left + right
            elif node.op == '-': result = left - right
            elif node.op == '*': result = left * right
            elif node.op == '/': result = left / right
            elif node.op == '<': result = left < right
            elif node.op == '>': result = left > right
            elif node.op == '<=': result = left <= right
            elif node.op == '>=': result = left >= right
            elif node.op == '==': result = left == right
            elif node.op == '!=': result = left != right

            self.log(f"Computed {left} {node.op} {right} = {result}")
            self.depth -= 1
            return result

        elif isinstance(node, Block):
            self.log("Block start")
            self.depth += 1

            for stmt in node.statements:
                self.eval(stmt)

            self.depth -= 1
            self.log("Block end")

        elif isinstance(node, If):
            self.log("If condition")
            self.depth += 1

            cond = self.eval(node.cond)

            self.depth -= 1

            if cond:
                self.log("Then branch")
                return self.eval(node.then_branch)
            elif node.else_branch:
                self.log("Else branch")
                return self.eval(node.else_branch)