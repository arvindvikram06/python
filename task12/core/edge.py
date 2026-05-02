class Edge:
    def __init__(self, from_id, to_id, edge_type, props):
        # ID of the source node (start of the relationship)
        self.from_id = from_id

        # ID of the destination node (end of the relationship)
        self.to_id = to_id

        # Type of relationship
        # Example: "FRIENDS_WITH", "WORKS_AT"
        self.type = edge_type

        # Properties of the edge (optional)
        # Example: {"since": 2020}
        self.props = props

    def __repr__(self):
        # How the edge prints
        # Example: 1 -FRIENDS_WITH-> 2
        return f"{self.from_id} -{self.type}-> {self.to_id}"