from database import execute

# Handles lazy query building and execution
class QuerySet:
    def __init__(self, model):
        self.model = model
        self.filters = {}
        self.order = None

    # Add filter conditions to the query
    def filter(self, **kwargs):
        for key in kwargs:
            self.filters[key] = kwargs[key]
        return self

    # Set the sort order of the results
    def order_by(self, field):
        self.order = field
        return self

    # Build and execute the SQL query
    def all(self):
        table = self.model.__name__.lower()
        sql = f"SELECT * FROM {table}"
        values = []

        # Build WHERE clause
        if self.filters:
            sql += " WHERE "
            conditions = []
            for key, val in self.filters.items():
                if "__" in key:
                    field, op = key.split("__")
                    if op == "gte":
                        conditions.append(f"{field} >= ?")
                    elif op == "lte":
                        conditions.append(f"{field} <= ?")
                else:
                    conditions.append(f"{key} = ?")
                values.append(val)
            sql += " AND ".join(conditions)

        # Build ORDER BY clause
        if self.order:
            if self.order.startswith("-"):
                sql += f" ORDER BY {self.order[1:]} DESC"
            else:
                sql += f" ORDER BY {self.order} ASC"

        # Execute and map rows to model instances
        cursor = execute(sql, values)
        rows = cursor.fetchall()

        return [self.model(**dict(row)) for row in rows]