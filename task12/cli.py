import re
from core.graph import Graph
from storage.wal import WAL
from algorithm.traversal import shortest_path
from query.matcher import match_query


class CLI:
    def __init__(self):
        self.graph = Graph()
        self.wal = WAL()
        self.wal.replay(self.graph)

    def start(self):
        print("=== Graph DB Shell ===")

        while True:
            cmd = input("graphdb> ").strip()

            if cmd.startswith("CREATE NODE"):
                label = re.search(r'\((\w+):', cmd).group(1)
                props = eval(re.search(r'\{(.*)\}', cmd).group(0))

                node = self.graph.create_node(label, props)
                self.wal.log(f"NODE|{label}|{props}")

                print(f"Node created: {node}")

            elif cmd.startswith("CREATE EDGE"):
                ids = list(map(int, re.findall(r'\((\d+)\)', cmd)))
                edge_type = re.search(r':(\w+)', cmd).group(1)

                self.graph.create_edge(ids[0], ids[1], edge_type, {})
                self.wal.log(f"EDGE|{ids[0]}|{ids[1]}|{edge_type}|{{}}")

                print(f"Edge created: {ids[0]} -{edge_type}-> {ids[1]}")

            elif cmd.startswith("MATCH"):
                headers, rows = match_query(self.graph, cmd)

                print("| " + " | ".join(headers) + " |")
                print("-" * (len(headers) * 10))

                for r in rows:
                    print("| " + " | ".join(r) + " |")

                print(f"{len(rows)} rows returned")

            elif cmd.startswith("SHORTEST_PATH"):
                nums = list(map(int, re.findall(r'\d+', cmd)))
                path = shortest_path(self.graph, nums[0], nums[1])

                if not path:
                    print("No path")
                else:
                    print(" -> ".join(map(str, path)))
                    print(f"{len(path)-1} hops")

            elif cmd == "STATS":
                s = self.graph.stats()
                print(f"Nodes: {s['nodes']} | Edges: {s['edges']} | Indexes: {s['indexes']}")

            elif cmd == "EXIT":
                break

            else:
                print("Unknown command")