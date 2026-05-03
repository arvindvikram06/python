# Task 15: Event Sourcing & CQRS Order System

A sophisticated implementation of **Event Sourcing** and **Command Query Responsibility Segregation (CQRS)** patterns in **Python** to manage a robust order lifecycle.

---

## Features

- **Event Sourcing**
  - Captures every state change as a sequence of immutable events.
  - Reconstructs the current state of an aggregate by replaying its event history.

- **CQRS Architecture**
  - **Command Side**: Handles business logic and state transitions (Orders, Inventory).
  - **Query Side**: Maintains a optimized "Read Store" for high-performance data retrieval.

- **Aggregate Pattern**
  - Uses `OrderAggregate` to encapsulate business rules and ensure consistency.
  - Emits events like `OrderPlaced` and `InventoryReserved` when commands are processed.

- **Message Bus**
  - Decouples the write side from the read side using an asynchronous message bus.
  - Automatically notifies projection handlers, notification services, and analytics engines.

- **State Replay**
  - Specialized logic to rebuild aggregate state from a raw event stream for auditing or recovery.

---

## Tech Stack

- **Python 3**
- **Asyncio** (for message bus and handlers)
- **UUID** (for unique identification)

---

## Project Workflow

1. **Command Input**: A `PlaceOrderCommand` is sent to the system.
2. **Aggregate Logic**: The `OrderAggregate` validates the command and calculates the total.
3. **Event Generation**: The aggregate produces a set of events (`OrderPlaced`, `InventoryReserved`) representing the change.
4. **Persistence**: Events are stored in the `EventStore` as the "Source of Truth".
5. **Projection**: The `MessageBus` publishes events to `OrderDashboardProjection` which updates the `ReadStore`.
6. **Side Effects**: Simultaneously, `NotificationService` and `AnalyticsProjection` react to the events.
7. **Querying**: The user queries the `ReadStore` to see the current dashboard state, avoiding expensive event replays for every read.

---

## Architectural Logic

- **Immutability**: Once an event is appended to the store, it is never changed or deleted.
- **Separation of Concerns**: The logic to calculate a total (Command) is entirely separate from the logic to display a dashboard (Query).

---

## Installation

```bash
python main.py
```
