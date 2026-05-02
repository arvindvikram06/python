class WAL:
    def __init__(self, filename="wal.log"):
        # File where all operations are stored
        self.filename = filename

    def log(self, entry):
        """
        Append a new operation to WAL file
        """

        with open(self.filename, "a") as f:
            # Write operation as a new line
            f.write(entry + "\n")

    def replay(self, graph):
        """
        Rebuild graph from WAL file
        """

        try:
            with open(self.filename, "r") as f:
                for line in f:
                    # Apply each operation again
                    self._apply(line.strip(), graph)

        except FileNotFoundError:
            # If file doesn't exist → ignore
            pass

    def _apply(self, line, graph):
        """
        Convert log entry → actual graph operation
        """

        parts = line.split("|")

        # Example:
        # NODE|Person|{"name":"Alice"}

        if parts[0] == "NODE":
            label = parts[1]
            props = eval(parts[2])   # convert string → dict

            graph.create_node(label, props)

        # Example:
        # EDGE|1|2|FRIENDS_WITH|{}

        elif parts[0] == "EDGE":
            graph.create_edge(
                int(parts[1]),   # from_id
                int(parts[2]),   # to_id
                parts[3],        # edge type
                eval(parts[4])   # properties
            )