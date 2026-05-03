# Task 2: Real-Time Chat Server

A lightweight real-time chat server built with **Python** using **WebSockets** and **AsyncIO**. It supports multiple chat rooms, private messaging, and persistent message history.

---

## Features

- **Multiple Chat Rooms**
  - Users can join specific rooms and broadcast messages to all participants.
  
- **Private Messaging**
  - Supports direct messaging between users within the same room.

- **Live User Presence**
  - Maintains a real-time list of active users per room.

- **Persistent Message History**
  - All room and private messages are stored in **SQLite** for future retrieval.

- **Asynchronous Architecture**
  - Built with `asyncio` and `websockets` for high concurrency and low latency.

- **JSON Protocol**
  - Uses a structured JSON-based protocol for all client-server communication.

---

## Tech Stack

- **Python 3**
- **AsyncIO**
- **Websockets**
- **SQLite3**
- **JSON**

---

## Project Workflow

1. **Connection**: Client establishes a WebSocket connection to the server.
2. **Identification**: Client sends a "join" message with their username and target room.
3. **Broadcasting**: Messages sent to a room are relayed to all active participants in that room.
4. **Private Routing**: Private messages are routed directly to the recipient based on their unique session ID.
5. **Persistence**: Every message is asynchronously written to the SQLite database.
6. **Disconnection**: The server detects closed sockets and removes users from the active lists.

---

## Server Logic

- **State Management**: Uses dictionaries to track active connections and room memberships in memory.
- **Async Loops**: Manages multiple concurrent connections without blocking using the `asyncio` event loop.

---

## Installation

```bash
pip install websockets
python server.py
```