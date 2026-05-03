from ast_nodes import *

# Executes the Abstract Syntax Tree (AST) recursively
class Interpreter:
    def __init__(self):
        # Variable storage (symbol table)
        self.env = {}

    # Main evaluation function
    def eval(self, node):
        # Numbers: Return the raw value
        if isinstance(node, Number):
            return node.value

        # Variables: Lookup in environment
        elif isinstance(node, Var):
            return self.env[node.name]

        # Assignments: Eval value and store in environment
        elif isinstance(node, Assign):
            value = self.eval(node.value)
            self.env[node.name] = value
            return value
        
        # While loops: Continuous evaluation of condition and body
        elif isinstance(node, While):
            while self.eval(node.cond):
                self.eval(node.body)

        # Binary Operations: Eval sides and apply operator
        elif isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == '+': return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left * right
            elif node.op == '/': return left / right
            elif node.op == '<': return left < right
            elif node.op == '>': return left > right
            elif node.op == '<=': return left <= right
            elif node.op == '>=': return left >= right
            elif node.op == '==': return left == right
            elif node.op == '!=': return left != right

        # Blocks: Execute each statement in sequence
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.eval(stmt)

        # If Statements: Conditional branch execution
        elif isinstance(node, If):
            if self.eval(node.cond):
                return self.eval(node.then_branch)
            elif node.else_branch:
                return self.eval(node.else_branch)