import asyncio

from commands.place_order import PlaceOrderCommand
from aggregates.order import OrderAggregate
from event_store.store import EventStore
from bus.message_bus import MessageBus

from handlers.projections import OrderDashboardProjection
from handlers.notifications import NotificationService
from handlers.analytics import AnalyticsProjection

from read_model.read_store import ReadStore
from replay.replay import replay


async def main():
    # Initialize components
    event_store = EventStore() 
    bus = MessageBus()         
    read_store = ReadStore()   

    # Register handlers
    projection = OrderDashboardProjection(read_store)
    notification = NotificationService()
    analytics = AnalyticsProjection()

    bus.register(projection)
    bus.register(notification)
    bus.register(analytics)

    # Create a command
    cmd = PlaceOrderCommand(
        "C-42",
        [
            {"sku": "WIDGET-01", "qty": 3, "price": 29.99},
            {"sku": "GADGET-05", "qty": 1, "price": 149.99},
        ],
    )

    # Process command on write side
    print("\n=== COMMAND SIDE ===")
    agg = OrderAggregate().place_order(cmd)
    
    # Save events to store
    event_store.append(agg.id, agg.changes)

    # Dispatch events to handlers
    print("\n=== EVENT HANDLERS ===")
    await bus.publish(agg.changes)

    # Query the current state
    print("\n=== QUERY SIDE ===")
    result = read_store.get(agg.id)
    print(f"Read Store Record: {result}")

    # Rebuild state from history
    print("\n=== REPLAY ===")
    events = event_store.get_events(agg.id)
    rebuilt = replay(events)

    print(f"Rebuilt Order: {rebuilt.id}, Total: {rebuilt.total}, Status: {rebuilt.status}")


if __name__ == "__main__":
    asyncio.run(main())