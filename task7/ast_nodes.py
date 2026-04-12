class Number:
    def __init__(self, value):
        self.value = int(value)
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class Var:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"