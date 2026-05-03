class Event:
    pass

# Represents a placed order
class OrderPlaced(Event):
    def __init__(self, order_id, customer, total):
        self.order_id = order_id
        self.customer = customer
        self.total = total

# Represents reserved inventory
class InventoryReserved(Event):
    def __init__(self, sku, qty):
        self.sku = sku
        self.qty = qty

class OrderUpdated(Event):
    def __init__(self, removed_item, new_total):
        self.removed_item = removed_item
        self.new_total = new_total

class PaymentProcessed(Event):
    def __init__(self, amount, method):
        self.amount = amount
        self.method = method

class OrderShipped(Event):
    def __init__(self, tracking):
        self.tracking = tracking