# Task 12: Graph Database with Shortest Path

A custom graph database implementation in **Python** featuring an interactive shell, Write-Ahead Logging (WAL) for persistence, and advanced pathfinding algorithms.

---

## Features

- **Interactive Query Shell**
  - Supports custom query language commands like `CREATE NODE`, `CREATE EDGE`, and `MATCH`.
  - Real-time feedback and data visualization in a tabular format.

- **Persistence with Write-Ahead Logging (WAL)**
  - All mutations (nodes and edges) are logged to a `wal.log` file.
  - Automatically replays logs on startup to restore the database state.

- **Pathfinding Algorithms**
  - Implements **Breadth-First Search (BFS)** to find the shortest path between any two nodes.
  - Supports `SHORTEST_PATH` command to calculate hops and visualize the route.

- **Schema-free Graph Model**
  - Nodes and edges can have arbitrary key-value properties.
  - Supports labeled edges for rich relationship modeling.

- **Query Matcher**
  - Advanced matching logic to retrieve nodes and relationships based on labels and attributes.

---

## Tech Stack

- **Python 3**
- **Collections** (Deque for BFS)
- **Regex** (for command parsing)

---

## Project Workflow

1. **Startup**: The system initializes the `Graph` and the `WAL` manager.
2. **Replay**: The `WAL` reads `wal.log` and recreates all nodes and edges in memory.
3. **User Interaction**: The user enters commands via the `graphdb>` shell.
4. **Command Processing**:
   - `CREATE NODE`: Adds a vertex to the graph and logs it to disk.
   - `CREATE EDGE`: Links two nodes with a specific relationship type.
   - `MATCH`: Queries the graph for specific patterns.
   - `SHORTEST_PATH`: Executes BFS to find the most efficient connection.
5. **Stats**: Display the current count of nodes, edges, and indexes.

---

## Graph Logic

- **Adjacency List**: Efficiently stores graph structure for fast traversal.
- **BFS Traversal**: Guarantees the shortest path in an unweighted graph by exploring all neighbors at the current depth before moving deeper.

---

## Installation

```bash
python main.py
```
