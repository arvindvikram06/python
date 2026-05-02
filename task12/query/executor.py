def execute(graph, tokens):
    if tokens[0] == "FIND":
        key, value = tokens[1].split("=")
        return graph.find_by_property(key, value)

    return []