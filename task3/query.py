from database import execute

class QuerySet:
    def __init__(self, model):
        self.model = model
        self.filters = {}
        self.order = None

    def filter(self, **kwargs):
        for key in kwargs:
            self.filters[key] = kwargs[key]
        return self

    def order_by(self, field):
        self.order = field
        return self

    def all(self):
        table = self.model.__name__.lower()
        sql = "SELECT * FROM " + table

        values = []

        if self.filters:
            sql += " WHERE "
            first = True

            for key in self.filters:
                if not first:
                    sql += " AND "

                if "__" in key:
                    parts = key.split("__")
                    field = parts[0]
                    op = parts[1]

                    if op == "gte":
                        sql += field + " >= ?"
                    elif op == "lte":
                        sql += field + " <= ?"
                else:
                    sql += key + " = ?"

                values.append(self.filters[key])
                first = False

        if self.order:
            if self.order.startswith("-"):
                sql += " ORDER BY " + self.order[1:] + " DESC"
            else:
                sql += " ORDER BY " + self.order + " ASC"

        # print(sql)

        cursor = execute(sql, values)
        rows = cursor.fetchall()

        result = []
        for row in rows:
            obj = self.model(**dict(row))
            result.append(obj)

        return result