class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"User: {self.name}, Age: {self.age}"

    def __repr__(self):
        return f"User(name='{self.name}', age={self.age})"


u = User("Alice", 25)

print(u)        # calls __str__
print(repr(u))  # calls __repr__