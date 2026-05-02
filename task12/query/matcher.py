import re


def match_query(graph, query):

    # WHERE
    where_match = re.search(r'WHERE (.+)', query)
    where = where_match.group(1) if where_match else None

    # MATCH pattern
    pattern_match = re.search(r'MATCH (.+?)( WHERE| RETURN|$)', query)
    pattern = pattern_match.group(1)

    # RETURN
    return_match = re.search(r'RETURN (.+)', query)
    returns = return_match.group(1).split(",") if return_match else []

    # Parse nodes and edges
    parts = re.findall(r'\((.*?)\)|\[:(.*?)\]', pattern)

    nodes = []
    edges = []

    for n, e in parts:
        if n:
            nodes.append(n)
        if e:
            edges.append(e)

    # Start node
    start = nodes[0]
    var, label = start.split(":") if ":" in start else (start, None)

    candidates = list(graph.nodes.values())

    if label:
        candidates = [n for n in candidates if n.label == label]

    results = []

    for node in candidates:
        paths = [(node.id, {var: node})]

        for i, edge_type in enumerate(edges):
            next_paths = []

            for nid, context in paths:
                for e in graph.adj[nid]:
                    if e.type != edge_type:
                        continue

                    next_node = graph.nodes[e.to_id]

                    var_name, label_name = nodes[i + 1].split(":") if ":" in nodes[i + 1] else (nodes[i + 1], None)

                    if label_name and next_node.label != label_name:
                        continue

                    new_ctx = context.copy()
                    new_ctx[var_name] = next_node

                    next_paths.append((next_node.id, new_ctx))

            paths = next_paths

        results.extend([ctx for _, ctx in paths])

    # Apply WHERE
    if where:
        key, val = where.split("=")
        key = key.strip()
        val = val.strip().strip('"')

        var, prop = key.split(".")

        results = [
            r for r in results
            if r[var].props.get(prop) == val
        ]

    # Build output
    headers = [r.strip() for r in returns]
    rows = []

    for r in results:
        row = []
        for h in headers:
            var, prop = h.split(".")
            row.append(str(r[var].props.get(prop)))
        rows.append(row)

    return headers, rows