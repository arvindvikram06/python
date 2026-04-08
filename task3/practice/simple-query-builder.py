class Query:
    def __init__(self, table):
        self.table = table
        self.conditions = []
        self.order = None

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            self.conditions.append(f"{key} = '{value}'")
        return self

    def order_by(self, field):
        self.order = field
        return self

    def build(self):
        sql = f"SELECT * FROM {self.table}"

        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)

        if self.order:
            sql += f" ORDER BY {self.order}"

        return sql


q = Query("user").filter(name="Alice").filter(age=25).order_by("name")
print(q.build())