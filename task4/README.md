# Distributed Task Queue

A lightweight distributed task queue built with **Python**, **Redis**, and **TCP sockets**. It supports delayed retries with exponential backoff, a dead letter queue, real-time events, and a CLI dashboard.

---

## Features

- **Socket-based Producer**
  - Accepts task submissions over a high-speed TCP connection.
  
- **Redis-backed Queues**
  - Uses Redis lists for the main queue and sorted sets for delayed tasks.
  - Implements a **Dead Letter Queue (DLQ)** for permanently failed tasks.

- **Multiprocessing Workers**
  - Concurrent task execution across multiple worker processes for high throughput.

- **Resilience & Retries**
  - Implements exponential backoff (`2^retries`) for failed tasks.
  - Automatically moves tasks to DLQ after exceeding `MAX_RETRIES`.

- **Real-time Monitoring**
  - Pub/Sub event bus for live status updates.
  - Interactive CLI dashboard for tracking task duration and status.

---

## Tech Stack

- **Python 3**
- **Redis**
- **TCP Sockets**
- **Multiprocessing**
- **JSON** (for message serialization)

---

## Project Workflow

1. **Submission**: The `client.py` sends a task to the `producer_server.py` via a TCP socket.
2. **Enqueue**: The producer receives the task and pushes it into the Redis queue.
3. **Consumption**: `worker.py` instances pop tasks from Redis and execute the corresponding function in `tasks.py`.
4. **Execution Tracking**: Workers publish events (SUCCESS, RETRY, DEAD) to a Redis channel.
5. **Recovery**: If a task fails, the `retry_manager.py` calculates the delay and re-queues it.
6. **Monitoring**: The `dashboard_server.py` (or `dashboard.py`) subscribes to events and displays a live feed to the user.

---

## Task Lifecycle

- **PENDING**: Task is in the main Redis queue waiting for a worker.
- **EXECUTING**: A worker has picked up the task and is running it.
- **SUCCESS**: Task completed successfully; results are stored.
- **RETRY**: Task failed but has remaining attempts; queued with exponential delay.
- **DEAD**: Task failed all attempts; moved to the Dead Letter Queue.

---

## Installation

```bash
# Ensure Redis is running
redis-server

# Start the worker pool
python worker.py

# Start the producer server
python producer_server.py

# Run the dashboard
python dashboard_server.py

# Submit a task
python client.py
```