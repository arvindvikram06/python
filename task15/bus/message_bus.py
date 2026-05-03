import asyncio

# Distributes events to all interested handlers
class MessageBus:
    def __init__(self):
        self.handlers = []

    # Add a new subscriber
    def register(self, handler):
        self.handlers.append(handler)

    # Publish events to handlers
    async def publish(self, events):
        print(f"[BUS] Publishing {len(events)} events...")
        tasks = []

        for handler in self.handlers:
            for event in events:
                tasks.append(handler.handle(event))

        await asyncio.gather(*tasks)