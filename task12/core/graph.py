from collections import defaultdict
from core.node import Node
from core.edge import Edge


class Graph:
    def __init__(self):
        self.nodes = {}
        self.adj = defaultdict(list)
        self.node_counter = 1

        # index: property -> value -> nodes
        self.index = defaultdict(lambda: defaultdict(list))

    def create_node(self, label, props):
        node = Node(self.node_counter, label, props)
        self.nodes[self.node_counter] = node
        self.adj[self.node_counter] = []

        # index
        for k, v in props.items():
            self.index[k][v].append(node)

        self.node_counter += 1
        return node

    def create_edge(self, from_id, to_id, edge_type, props):
        edge = Edge(from_id, to_id, edge_type, props)
        self.adj[from_id].append(edge)
        return edge

    def find_nodes(self, key, value):
        return self.index.get(key, {}).get(value, [])

    def stats(self):
        edge_count = sum(len(v) for v in self.adj.values())
        return {
            "nodes": len(self.nodes),
            "edges": edge_count,
            "indexes": len(self.index)
        }