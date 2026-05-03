from collections import deque


def shortest_path(graph, start, end):
    # Queue for BFS (FIFO structure)
    queue = deque([start])

    # Set to keep track of visited nodes
    visited = {start}

    # Dictionary to remember path
    # child → parent
    parent = {}

    while queue:
        # Get next node
        curr = queue.popleft()

        # If we reached destination → stop
        if curr == end:
            break

        # Explore neighbors
        for edge in graph.adj[curr]:
            # If not visited
            if edge.to_id not in visited:
                visited.add(edge.to_id)

                # Remember how we reached this node
                parent[edge.to_id] = curr

                queue.append(edge.to_id)

    # If no path found
    if end not in parent and start != end:
        return []

    # Reconstruct path
    path = []
    curr = end

    while curr != start:
        path.append(curr)
        curr = parent.get(curr)

        if curr is None:
            return []

    path.append(start)

    # Reverse path (because we built it backwards)
    return path[::-1]from collections import deque


def shortest_path(graph, start, end):
    # Queue for BFS (FIFO structure)
    queue = deque([start])

    # Set to keep track of visited nodes
    visited = {start}

    # Dictionary to remember path
    # child → parent
    parent = {}

    while queue:
        # Get next node
        curr = queue.popleft()

        # If we reached destination → stop
        if curr == end:
            break

        # Explore neighbors
        for edge in graph.adj[curr]:
            # If not visited
            if edge.to_id not in visited:
                visited.add(edge.to_id)

                # Remember how we reached this node
                parent[edge.to_id] = curr

                queue.append(edge.to_id)

    # If no path found
    if end not in parent and start != end:
        return []

    # Reconstruct path (VERY IMPORTANT PART)
    path = []
    curr = end

    while curr != start:
        path.append(curr)
        curr = parent.get(curr)

        if curr is None:
            return []

    path.append(start)

    # Reverse path (because we built it backwards)
    return path[::-1]