class Node:
    def __init__(self, node_id, label, props):
        # Unique ID for the node (auto-incremented in Graph)
        self.id = node_id

        # Label/type of node (e.g., "Person", "Company")
        self.label = label

        # Dictionary storing properties
        # Example: {"name": "Alice", "age": 30}
        self.props = props

    def __repr__(self):
        # This defines how the node is printed
        # Example output: Person#1
        return f"{self.label}#{self.id}"