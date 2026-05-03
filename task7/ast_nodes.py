# Node for literal numbers
class Number:
    def __init__(self, value):
        self.value = int(value)
    def __repr__(self):
        return f"Number({self.value})"

# Node for variable identifiers
class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

# Node for binary operations (a + b, x < 5)
class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

# Node for variable assignments (x = 10)
class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Assign({self.name}, {self.value})"

# Node for conditional If statements
class If:
    def __init__(self, cond, then_branch, else_branch=None):
        self.cond = cond
        self.then_branch = then_branch
        self.else_branch = else_branch

# Node for a group of statements
class Block:
    def __init__(self, statements):
        self.statements = statements

# Node for while loop structures
class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
