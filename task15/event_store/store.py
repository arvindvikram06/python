# Permanent storage of events
class EventStore:
    def __init__(self):
        # { aggregate_id: [events] }
        self.store = {}

    # Save new events
    def append(self, aggregate_id, events):
        if aggregate_id not in self.store:
            self.store[aggregate_id] = []

        self.store[aggregate_id].extend(events)

        print("[EVENT STORE] Appended events:")
        for i, e in enumerate(events, 1):
            print(f"  {i}. {e.__class__.__name__} {vars(e)}")

    # Get history for an aggregate
    def get_events(self, aggregate_id):
        return self.store.get(aggregate_id, [])