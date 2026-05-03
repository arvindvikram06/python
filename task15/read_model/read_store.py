# Database optimized for queries
class ReadStore:
    def __init__(self):
        # Current state of orders
        self.db = {}

    # Update or insert record
    def insert(self, data):
        self.db[data["order_id"]] = data

    # Lookup by ID
    def get(self, order_id):
        return self.db.get(order_id)