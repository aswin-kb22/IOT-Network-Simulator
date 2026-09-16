class Topology:

    def __init__(self, canvas):
        self.canvas = canvas
        self.nodes = {}
        self.connections = {}

    def add_sensor_node(self, sensor):
        x = 100
        y = 100 + (len(self.nodes) * 80)

        node_id = sensor.get_device_id()

        node = self.canvas.create_oval(
            x - 30, y - 30,
            x + 30, y + 30
        )

        label = self.canvas.create_text(
            x, y,
            text=f"Sensor\n{node_id}"
        )

        self.nodes[node_id] = {
            "type": "sensor",
            "x": x,
            "y": y,
            "shape": node,
            "label": label
        }

    def add_gateway_node(self, gateway):
        x = 400
        y = 200

        node_id = gateway.get_device_id()

        node = self.canvas.create_rectangle(
            x - 45, y - 30,
            x + 45, y + 30
        )

        label = self.canvas.create_text(
            x, y,
            text=f"Gateway\n{node_id}"
        )

        self.nodes[node_id] = {
            "type": "gateway",
            "x": x,
            "y": y,
            "shape": node,
            "label": label
        }

    def add_server_node(self, server):
        x = 700
        y = 200

        node_id = server.get_device_id()

        node = self.canvas.create_rectangle(
            x - 45, y - 30,
            x + 45, y + 30
        )

        label = self.canvas.create_text(
            x, y,
            text=f"Server\n{node_id}"
        )

        self.nodes[node_id] = {
            "type": "server",
            "x": x,
            "y": y,
            "shape": node,
            "label": label
        }

    def connect_nodes(self, source, destination):
        source_id = source.get_device_id()
        destination_id = destination.get_device_id()

        if source_id not in self.nodes or destination_id not in self.nodes:
            return

        source_node = self.nodes[source_id]
        destination_node = self.nodes[destination_id]

        line = self.canvas.create_line(
            source_node["x"],
            source_node["y"],
            destination_node["x"],
            destination_node["y"]
        )

        connection_id = f"{source_id}->{destination_id}"

        self.connections[connection_id] = line

    def remove_node(self, device_id):
        if device_id not in self.nodes:
            return

        node = self.nodes[device_id]

        self.canvas.delete(node["shape"])
        self.canvas.delete(node["label"])

        # Remove connections involving this node
        connections_to_remove = []

        for connection_id in self.connections:
            if (
                connection_id.startswith(device_id + "->")
                or connection_id.endswith("->" + device_id)
            ):
                connections_to_remove.append(connection_id)

        for connection_id in connections_to_remove:
            self.canvas.delete(
                self.connections[connection_id]
            )
            del self.connections[connection_id]

        del self.nodes[device_id]

    def update_node_status(self, device_id, status):
        if device_id not in self.nodes:
            return

        node = self.nodes[device_id]

        if status == "ACTIVE":
            # Normal appearance
            self.canvas.itemconfig(
                node["shape"],
                state="normal"
            )

        elif status == "INACTIVE":
            # Keep the node visible but visually disable it
            self.canvas.itemconfig(
                node["shape"],
                state="disabled"
            )

    def clear_topology(self):
        self.canvas.delete("all")

        self.nodes.clear()
        self.connections.clear()