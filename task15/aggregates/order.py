import uuid
from events.events import OrderPlaced, InventoryReserved

class OrderAggregate:
    def __init__(self):
        # Order state
        self.id = None
        self.customer = None
        self.total = 0
        self.items = []
        self.status = "CREATED"
        
        # New events generated
        self.changes = []

    # Update state based on an event
    def apply(self, event):
        if isinstance(event, OrderPlaced):
            self.id = event.order_id
            self.customer = event.customer
            self.total = event.total
            self.status = "PLACED"

    # Logic to process order placement
    def place_order(self, command):
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        total = sum(i["qty"] * i["price"] for i in command.items)

        # Create and apply events
        event = OrderPlaced(order_id, command.customer_id, total)
        self.apply(event)
        self.changes.append(event)

        # Reserve inventory
        for item in command.items:
            inv_event = InventoryReserved(item["sku"], item["qty"])
            self.changes.append(inv_event)

        return self