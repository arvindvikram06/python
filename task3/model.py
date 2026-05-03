from database import execute
from fields import Field, ForeignKey
from query import QuerySet

# Base class for all database models
class Model:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        
        # Initialize fields from keyword arguments
        for key, attr in self.__class__.__dict__.items():
            if isinstance(attr, Field):
                setattr(self, key, kwargs.get(key))

    # Creates the database table for the model
    @classmethod
    def create_table(cls):
        table = cls.__name__.lower()
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for key, attr in cls.__dict__.items():
            if isinstance(attr, Field):
                columns.append(attr.get_sql())

        sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
        execute(sql)
        print("Table created:", table)

    # Inserts the current instance into the database
    def save(self):
        table = self.__class__.__name__.lower()
        fields, values, placeholders = [], [], []

        for key, attr in self.__class__.__dict__.items():
            if isinstance(attr, Field):
                if isinstance(attr, ForeignKey):
                    fields.append(key + "_id")   
                    values.append(getattr(self, attr.private_name, None))
                else:
                    fields.append(key)
                    values.append(getattr(self, key))
                placeholders.append("?")

        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
        cursor = execute(sql, values)
        self.id = cursor.lastrowid
        print("Saved:", self)

    # Deletes the current instance from the database
    def delete(self):
        table = self.__class__.__name__.lower()
        sql = f"DELETE FROM {table} WHERE id = ?"
        execute(sql, [self.id])

    # Returns a QuerySet for filtering results
    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)

    # Retrieves a single instance matching the criteria
    @classmethod
    def get(cls, **kwargs):
        results = cls.filter(**kwargs).all()
        return results[0] if results else None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"