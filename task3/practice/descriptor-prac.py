class Field:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        value = self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value):
        return value


class CharField(Field):
    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError("Must be string")
        if len(value) > self.max_length:
            raise ValueError("Too long")
        return value


class User:
    name = CharField(10)


# # demo
# u = User()
# u.name = "Alice"
# print(u.name)

# # error case
# try:
#     u.name = "This is too long"
# except Exception as e:
#     print("Error:", e)