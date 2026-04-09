class Field:
    def __init__(self, column_type, nullable=False):
        print(f"init called ${column_type}")
        self.column_type = column_type
        self.nullable = nullable

    def __set_name__(self, owner, name):
        print(self)
        print(f"called set_name in field ${name}")
        self.name = name
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        print(f"__get__ called for {self.name}")
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        print(f"__set__ called for {self.name}: {value}")
        value = self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value):
        return value

    def get_sql(self):
        sql = self.name + " " + self.column_type
        if not self.nullable:
            sql += " NOT NULL"
        return sql


class CharField(Field):
    def __init__(self, max_length, nullable=False):
        super().__init__("VARCHAR(" + str(max_length) + ")", nullable)
        self.max_length = max_length

    def validate(self, value):
        if value is None:
            if self.nullable:
                return value
            raise ValueError(self.name + " cannot be None")

        if not isinstance(value, str):
            raise TypeError(self.name + " must be string")

        if len(value) > self.max_length:
            raise ValueError(self.name + " too long")

        return value


class IntegerField(Field):
    def __init__(self, nullable=False):
        super().__init__("INTEGER", nullable)

    def validate(self, value):
        if value is None:
            if self.nullable:
                return value
            raise ValueError(self.name + " cannot be None")

        if not isinstance(value, int):
            raise TypeError(self.name + " must be int")

        return value




# class User:
#     name = CharField(10)


# u = User()

# u.name = "Arvind"

# print(User.name.get_sql())