from events.events import OrderPlaced

# Tracks global system metrics
class AnalyticsProjection:
    def __init__(self):
        self.revenue = 0

    async def handle(self, event):
        if isinstance(event, OrderPlaced):
            self.revenue += event.total
            print(f"[HANDLER: Analytics] Revenue updated: ${self.revenue}")