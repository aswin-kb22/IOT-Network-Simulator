import tkinter as tk


class Topology:
    """
    Handles the visual representation of the IoT network topology.

    Nodes:
        - Sensors
        - Gateway
        - Server

    The topology is drawn using a Tkinter Canvas.
    """

    def __init__(self, canvas):
        """
        Initialize the topology.

        Parameters:
            canvas (tk.Canvas): Canvas on which the topology is drawn.
        """

        self.canvas = canvas

        # Store node information.
        #
        # Format:
        # {
        #     device_id: {
        #         "type": "sensor",
        #         "x": 100,
        #         "y": 200,
        #         "shape": canvas_id,
        #         "label": canvas_id,
        #         "status": "ACTIVE"
        #     }
        # }
        self.nodes = {}

        # Store connections.
        #
        # Format:
        # {
        #     (source_id, destination_id): canvas_line_id
        # }
        self.connections = {}

        # Default node positions.
        self.sensor_start_x = 120
        self.sensor_start_y = 120

        self.sensor_spacing_x = 150
        self.sensor_spacing_y = 100

        self.gateway_position = (450, 300)
        self.server_position = (750, 300)

        # Number of sensors currently created.
        self.sensor_count = 0

        # Node dimensions.
        self.node_width = 80
        self.node_height = 50

    # =========================================================
    # SENSOR NODE
    # =========================================================

    def add_sensor_node(self, sensor):
        """
        Add a sensor node to the topology.

        Parameters:
            sensor:
                Sensor object containing a device ID.

        Returns:
            str/int:
                The device ID of the created sensor node.
        """

        device_id = self._get_device_id(sensor)

        # Prevent duplicate nodes.
        if device_id in self.nodes:
            return device_id

        # Calculate position automatically.
        x, y = self._get_sensor_position()

        status = self._get_status(sensor)

        # Draw sensor.
        shape = self.canvas.create_oval(
            x - self.node_width / 2,
            y - self.node_height / 2,
            x + self.node_width / 2,
            y + self.node_height / 2,
            fill="lightblue",
            outline="black",
            width=2,
            tags="sensor"
        )

        # Draw label.
        label = self.canvas.create_text(
            x,
            y,
            text=str(device_id),
            font=("Arial", 10, "bold"),
            tags="sensor_label"
        )

        # Store node.
        self.nodes[device_id] = {
            "type": "sensor",
            "x": x,
            "y": y,
            "shape": shape,
            "label": label,
            "status": status,
            "object": sensor
        }

        self.sensor_count += 1

        return device_id

    # =========================================================
    # GATEWAY NODE
    # =========================================================

    def add_gateway_node(self, gateway):
        """
        Add a gateway node to the topology.

        Parameters:
            gateway:
                Gateway object.

        Returns:
            str/int:
                Gateway device ID.
        """

        device_id = self._get_device_id(gateway)

        if device_id in self.nodes:
            return device_id

        x, y = self.gateway_position

        status = self._get_status(gateway)

        # Draw gateway as a rectangle.
        shape = self.canvas.create_rectangle(
            x - self.node_width / 2,
            y - self.node_height / 2,
            x + self.node_width / 2,
            y + self.node_height / 2,
            fill="lightyellow",
            outline="black",
            width=2,
            tags="gateway"
        )

        label = self.canvas.create_text(
            x,
            y,
            text=str(device_id),
            font=("Arial", 10, "bold"),
            tags="gateway_label"
        )

        self.nodes[device_id] = {
            "type": "gateway",
            "x": x,
            "y": y,
            "shape": shape,
            "label": label,
            "status": status,
            "object": gateway
        }

        return device_id

    # =========================================================
    # SERVER NODE
    # =========================================================

    def add_server_node(self, server):
        """
        Add a server node to the topology.

        Parameters:
            server:
                Server object.

        Returns:
            str/int:
                Server device ID.
        """

        device_id = self._get_device_id(server)

        if device_id in self.nodes:
            return device_id

        x, y = self.server_position

        status = self._get_status(server)

        # Draw server as a rectangle.
        shape = self.canvas.create_rectangle(
            x - self.node_width / 2,
            y - self.node_height / 2,
            x + self.node_width / 2,
            y + self.node_height / 2,
            fill="lightgreen",
            outline="black",
            width=2,
            tags="server"
        )

        label = self.canvas.create_text(
            x,
            y,
            text=str(device_id),
            font=("Arial", 10, "bold"),
            tags="server_label"
        )

        self.nodes[device_id] = {
            "type": "server",
            "x": x,
            "y": y,
            "shape": shape,
            "label": label,
            "status": status,
            "object": server
        }

        return device_id

    # =========================================================
    # CONNECT NODES
    # =========================================================

    def connect_nodes(self, source, destination):
        """
        Draw a connection between two nodes.

        Parameters:
            source:
                Source device or device ID.

            destination:
                Destination device or device ID.

        Returns:
            tuple:
                Connection key.
        """

        source_id = self._get_device_id(source)
        destination_id = self._get_device_id(destination)

        # Both nodes must exist.
        if source_id not in self.nodes:
            raise ValueError(
                f"Source node '{source_id}' does not exist."
            )

        if destination_id not in self.nodes:
            raise ValueError(
                f"Destination node '{destination_id}' does not exist."
            )

        # Do not connect a node to itself.
        if source_id == destination_id:
            raise ValueError(
                "A node cannot be connected to itself."
            )

        connection_key = (
            source_id,
            destination_id
        )

        # Don't create duplicate connection.
        if connection_key in self.connections:
            return connection_key

        source_node = self.nodes[source_id]
        destination_node = self.nodes[destination_id]

        # Draw connection line.
        line = self.canvas.create_line(
            source_node["x"],
            source_node["y"],
            destination_node["x"],
            destination_node["y"],
            fill="gray",
            width=2,
            tags="connection"
        )

        # Send connection behind nodes.
        self.canvas.tag_lower(line)

        self.connections[connection_key] = line

        return connection_key

    # =========================================================
    # REMOVE NODE
    # =========================================================

    def remove_node(self, device_id):
        """
        Remove a node and its connections.

        Parameters:
            device_id:
                ID of the device to remove.
        """

        if device_id not in self.nodes:
            return

        node = self.nodes[device_id]

        # Delete node shape.
        self.canvas.delete(
            node["shape"]
        )

        # Delete node label.
        self.canvas.delete(
            node["label"]
        )

        # Find all connections involving this node.
        connections_to_remove = []

        for connection in self.connections:

            source_id, destination_id = connection

            if (
                source_id == device_id
                or destination_id == device_id
            ):
                connections_to_remove.append(
                    connection
                )

        # Remove connections.
        for connection in connections_to_remove:

            line = self.connections[
                connection
            ]

            self.canvas.delete(line)

            del self.connections[
                connection
            ]

        # Update sensor count.
        if node["type"] == "sensor":
            self.sensor_count = max(
                0,
                self.sensor_count - 1
            )

        # Remove from node dictionary.
        del self.nodes[device_id]

    # =========================================================
    # UPDATE NODE STATUS
    # =========================================================

    def update_node_status(self, device_id, status):
        """
        Update the visual status of a node.

        Parameters:
            device_id:
                Device identifier.

            status:
                New device status.
        """

        if device_id not in self.nodes:
            return

        node = self.nodes[device_id]

        node["status"] = status

        status_text = str(status).upper()

        # Choose color according to status.
        if status_text in (
            "ACTIVE",
            "RUNNING",
            "ONLINE"
        ):
            color = self._get_default_color(
                node["type"]
            )

        elif status_text in (
            "INACTIVE",
            "OFFLINE",
            "DISABLED"
        ):
            color = "lightgray"

        elif status_text in (
            "ERROR",
            "FAILED"
        ):
            color = "red"

        elif status_text in (
            "BUSY",
            "PROCESSING"
        ):
            color = "orange"

        else:
            color = self._get_default_color(
                node["type"]
            )

        # Change node color.
        self.canvas.itemconfig(
            node["shape"],
            fill=color
        )

    # =========================================================
    # CLEAR TOPOLOGY
    # =========================================================

    def clear_topology(self):
        """
        Remove all nodes and connections from the canvas.
        """

        # Delete everything managed by topology.
        self.canvas.delete("sensor")
        self.canvas.delete("sensor_label")

        self.canvas.delete("gateway")
        self.canvas.delete("gateway_label")

        self.canvas.delete("server")
        self.canvas.delete("server_label")

        self.canvas.delete("connection")

        # Clear internal data.
        self.nodes.clear()
        self.connections.clear()

        self.sensor_count = 0

    # =========================================================
    # GET NODE POSITION
    # =========================================================

    def get_node_position(self, device_id):
        """
        Get the canvas coordinates of a node.

        Parameters:
            device_id:
                Device identifier.

        Returns:
            tuple:
                (x, y) coordinates.

            None:
                If the node does not exist.
        """

        if device_id not in self.nodes:
            return None

        node = self.nodes[device_id]

        return (
            node["x"],
            node["y"]
        )

    # =========================================================
    # GET NODE
    # =========================================================

    def get_node(self, device_id):
        """
        Return stored information about a node.

        Parameters:
            device_id:
                Device identifier.

        Returns:
            dict or None:
                Node information.
        """

        return self.nodes.get(
            device_id
        )

    # =========================================================
    # GET ALL NODES
    # =========================================================

    def get_all_nodes(self):
        """
        Return all nodes in the topology.

        Returns:
            dict:
                Dictionary of all nodes.
        """

        return self.nodes.copy()

    # =========================================================
    # GET CONNECTIONS
    # =========================================================

    def get_connections(self):
        """
        Return all topology connections.

        Returns:
            dict:
                Dictionary of connections.
        """

        return self.connections.copy()

    # =========================================================
    # HELPER: DEVICE ID
    # =========================================================

    def _get_device_id(self, device):
        """
        Extract device ID from a device object or dictionary.

        Parameters:
            device:
                Device object, sensor, gateway, server,
                dictionary, or direct device ID.

        Returns:
            Device ID.
        """

        # Direct string/integer ID.
        if isinstance(
            device,
            (str, int)
        ):
            return device

        # Dictionary.
        if isinstance(device, dict):

            if "device_id" in device:
                return device["device_id"]

            if "id" in device:
                return device["id"]

        # Object.
        if hasattr(
            device,
            "device_id"
        ):
            return device.device_id

        if hasattr(
            device,
            "id"
        ):
            return device.id

        raise ValueError(
            "Device must contain device_id or id."
        )

    # =========================================================
    # HELPER: STATUS
    # =========================================================

    def _get_status(self, device):
        """
        Extract device status.

        Parameters:
            device:
                Device object or dictionary.

        Returns:
            str:
                Device status.
        """

        if isinstance(device, dict):

            return device.get(
                "status",
                "ACTIVE"
            )

        if hasattr(
            device,
            "get_status"
        ):

            return device.get_status()

        if hasattr(
            device,
            "status"
        ):

            return device.status

        return "ACTIVE"

    # =========================================================
    # HELPER: SENSOR POSITION
    # =========================================================

    def _get_sensor_position(self):
        """
        Generate the next sensor position.

        Returns:
            tuple:
                (x, y) coordinates.
        """

        index = self.sensor_count

        # Maximum sensors per row.
        sensors_per_row = 4

        column = index % sensors_per_row
        row = index // sensors_per_row

        x = (
            self.sensor_start_x
            + column * self.sensor_spacing_x
        )

        y = (
            self.sensor_start_y
            + row * self.sensor_spacing_y
        )

        return x, y

    # =========================================================
    # HELPER: DEFAULT NODE COLOR
    # =========================================================

    def _get_default_color(self, node_type):
        """
        Return the default color for a node type.

        Parameters:
            node_type:
                sensor, gateway, or server.

        Returns:
            str:
                Tkinter color name.
        """

        colors = {
            "sensor": "lightblue",
            "gateway": "lightyellow",
            "server": "lightgreen"
        }

        return colors.get(
            node_type,
            "white"
        )
