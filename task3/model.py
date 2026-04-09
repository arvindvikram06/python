from database import execute
from fields import Field
from query import QuerySet

class Model:
    def __init__(self, **kwargs):
        print("called model init")
        self.id = kwargs.get("id")

        for key, attr in self.__class__.__dict__.items():
            if isinstance(attr, Field):
                print(f"Field detected -> {key}")

                setattr(self, key, kwargs.get(key))

    @classmethod
    def create_table(cls):
        table = cls.__name__.lower()
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for key, attr in cls.__dict__.items():
            if isinstance(attr, Field):
                columns.append(attr.get_sql())

        sql = "CREATE TABLE IF NOT EXISTS " + table + " ("
        sql += ", ".join(columns)
        sql += ")"

        execute(sql)
        print("Table created:", table)

    def save(self):
        table = self.__class__.__name__.lower()

        fields = []
        values = []
        placeholders = []

        for key, attr in self.__class__.__dict__.items():
            if isinstance(attr, Field):
                fields.append(key)
                values.append(getattr(self, key))  
                placeholders.append("?")

        sql = "INSERT INTO " + table
        sql += " (" + ", ".join(fields) + ")"
        sql += " VALUES (" + ", ".join(placeholders) + ")"

        print(sql)
        cursor = execute(sql, values)
        self.id = cursor.lastrowid

        print("Saved:", self)

    def delete(self):
        table = self.__class__.__name__.lower()
        sql = "DELETE FROM " + table + " WHERE id = ?"
        execute(sql, [self.id])

    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        results = cls.filter(**kwargs).all()
        return results[0] if results else None

    def __repr__(self):
        return self.__class__.__name__ + "(id=" + str(self.id) + ")"