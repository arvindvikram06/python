from aggregates.order import OrderAggregate

# Rebuilds aggregate state from history
def replay(events):
    agg = OrderAggregate()

    for event in events:
        agg.apply(event)

    return agg