class Field:
    def __init__(self, column_type):
        self.column_type = column_type

    def __set_name__(self, owner, name):
        self.name = name


class CharField(Field):
    def __init__(self):
        super().__init__("TEXT")


class IntegerField(Field):
    def __init__(self):
        super().__init__("INTEGER")


class Model:
    @classmethod
    def create_table(cls):
        columns = []

        for key, value in cls.__dict__.items():
            if isinstance(value, Field):
                columns.append(f"{value.name} {value.column_type}")

        sql = f"CREATE TABLE {cls.__name__.lower()} (id INTEGER PRIMARY KEY, "
        sql += ", ".join(columns) + ")"

        print(sql)


class User(Model):
    name = CharField()
    age = IntegerField()


User.create_table()