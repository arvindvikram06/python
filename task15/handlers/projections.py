from events.events import OrderPlaced

# Transforms events into a read model format
class OrderDashboardProjection:
    def __init__(self, read_store):
        self.read_store = read_store

    async def handle(self, event):
        if isinstance(event, OrderPlaced):
            print("[HANDLER: Dashboard] Updating read model...")

            # Format data for the read store
            self.read_store.insert({
                "order_id": event.order_id,
                "customer_id": event.customer,
                "total": event.total,
                "status": "PLACED",
                "item_count": 4 
            })