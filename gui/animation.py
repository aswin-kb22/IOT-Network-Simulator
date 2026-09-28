import tkinter as tk


class PacketAnimation:
    """
    Handles packet-flow animation on a Tkinter Canvas.

    The canvas is expected to contain the network topology.
    Source and destination can be:
        - dictionaries containing x/y coordinates
        - objects containing x/y attributes
        - tuples/lists in the form (x, y)
    """

    def __init__(self, canvas):
        """
        Initialize the packet animation manager.

        Parameters:
            canvas (tk.Canvas): Canvas used for drawing animations.
        """
        self.canvas = canvas

        # Stores packet_id -> canvas object ID
        self.packet_items = {}

        # Stores packet_id -> animation information
        self.animation_data = {}

        # Animation configuration
        self.animation_steps = 20
        self.animation_delay = 30

    # ---------------------------------------------------------
    # Animate packet
    # ---------------------------------------------------------

    def animate_packet(self, packet, source, destination):
        """
        Animate a packet from source to destination.

        Parameters:
            packet: Packet object containing packet information.
            source: Source device/coordinate.
            destination: Destination device/coordinate.

        Returns:
            int: Canvas object ID of the animated packet.
        """

        packet_id = self._get_packet_id(packet)

        source_position = self._get_position(source)
        destination_position = self._get_position(destination)

        if source_position is None or destination_position is None:
            raise ValueError(
                "Source and destination must contain valid coordinates."
            )

        # Remove an existing animation for the same packet
        if packet_id in self.packet_items:
            self.remove_packet(packet_id)

        start_x, start_y = source_position

        # Draw packet as a small circle
        packet_item = self.canvas.create_oval(
            start_x - 6,
            start_y - 6,
            start_x + 6,
            start_y + 6,
            fill="blue",
            outline="black",
            tags="packet"
        )

        self.packet_items[packet_id] = packet_item

        self.animation_data[packet_id] = {
            "source": source_position,
            "destination": destination_position,
            "step": 0
        }

        # Start animation
        self._move_packet(packet_id)

        return packet_item

    # ---------------------------------------------------------
    # Internal animation function
    # ---------------------------------------------------------

    def _move_packet(self, packet_id):
        """
        Move a packet by one animation step.

        Parameters:
            packet_id: ID of the packet being animated.
        """

        if packet_id not in self.packet_items:
            return

        if packet_id not in self.animation_data:
            return

        data = self.animation_data[packet_id]

        source_x, source_y = data["source"]
        destination_x, destination_y = data["destination"]

        step = data["step"]

        # Calculate progress from 0 to 1
        progress = step / self.animation_steps

        # Calculate current position
        current_x = (
            source_x +
            (destination_x - source_x) * progress
        )

        current_y = (
            source_y +
            (destination_y - source_y) * progress
        )

        self.update_packet_position(
            packet_id,
            (current_x, current_y)
        )

        # Continue animation
        if step < self.animation_steps:

            data["step"] += 1

            self.canvas.after(
                self.animation_delay,
                lambda: self._move_packet(packet_id)
            )

        else:
            # Packet reached destination
            self.show_packet_status(
                packet_id,
                "delivered"
            )

    # ---------------------------------------------------------
    # Update packet position
    # ---------------------------------------------------------

    def update_packet_position(self, packet_id, position):
        """
        Update the position of an animated packet.

        Parameters:
            packet_id: Packet identifier.
            position: Tuple containing (x, y).
        """

        if packet_id not in self.packet_items:
            return

        x, y = position

        packet_item = self.packet_items[packet_id]

        self.canvas.coords(
            packet_item,
            x - 6,
            y - 6,
            x + 6,
            y + 6
        )

        # Make sure the packet is visible
        self.canvas.tag_raise(packet_item)

    # ---------------------------------------------------------
    # Show packet status
    # ---------------------------------------------------------

    def show_packet_status(self, packet_id, status):
        """
        Change the visual appearance of a packet according
        to its current status.

        Parameters:
            packet_id: Packet identifier.
            status: Packet status.
        """

        if packet_id not in self.packet_items:
            return

        packet_item = self.packet_items[packet_id]

        status = str(status).lower()

        if status in ("created", "pending"):
            color = "blue"

        elif status in ("transmitting", "forwarded"):
            color = "orange"

        elif status in ("delivered", "received", "success"):
            color = "green"

        elif status in ("lost", "dropped", "failed"):
            color = "red"

        else:
            color = "gray"

        self.canvas.itemconfig(
            packet_item,
            fill=color
        )

    # ---------------------------------------------------------
    # Remove packet
    # ---------------------------------------------------------

    def remove_packet(self, packet_id):
        """
        Remove a packet from the canvas.

        Parameters:
            packet_id: Packet identifier.
        """

        if packet_id in self.packet_items:

            packet_item = self.packet_items[packet_id]

            self.canvas.delete(packet_item)

            del self.packet_items[packet_id]

        if packet_id in self.animation_data:
            del self.animation_data[packet_id]

    # ---------------------------------------------------------
    # Clear all animations
    # ---------------------------------------------------------

    def clear_animations(self):
        """
        Remove all currently animated packets.
        """

        for packet_item in self.packet_items.values():
            self.canvas.delete(packet_item)

        self.packet_items.clear()
        self.animation_data.clear()

    # ---------------------------------------------------------
    # Helper: get packet ID
    # ---------------------------------------------------------

    def _get_packet_id(self, packet):
        """
        Extract packet ID from a Packet object or dictionary.
        """

        if isinstance(packet, dict):

            if "packet_id" in packet:
                return packet["packet_id"]

            if "id" in packet:
                return packet["id"]

        if hasattr(packet, "packet_id"):
            return packet.packet_id

        if hasattr(packet, "id"):
            return packet.id

        raise ValueError(
            "Packet must contain packet_id or id."
        )

    # ---------------------------------------------------------
    # Helper: get coordinates
    # ---------------------------------------------------------

    def _get_position(self, device):
        """
        Extract x/y coordinates from a device.

        Supported formats:

            (x, y)

            {"x": x, "y": y}

            object.x and object.y
        """

        # Tuple/list
        if isinstance(device, (tuple, list)):

            if len(device) >= 2:
                return (
                    device[0],
                    device[1]
                )

        # Dictionary
        if isinstance(device, dict):

            if "x" in device and "y" in device:
                return (
                    device["x"],
                    device["y"]
                )

        # Object attributes
        if hasattr(device, "x") and hasattr(device, "y"):

            return (
                device.x,
                device.y
            )

        return None

    # ---------------------------------------------------------
    # Change animation speed
    # ---------------------------------------------------------

    def set_animation_speed(self, delay):
        """
        Change animation speed.

        Parameters:
            delay (int): Delay between animation frames in
                         milliseconds.
        """

        if delay <= 0:
            raise ValueError(
                "Animation delay must be greater than zero."
            )

        self.animation_delay = delay

    # ---------------------------------------------------------
    # Get active packet count
    # ---------------------------------------------------------

    def get_active_packet_count(self):
        """
        Return the number of packets currently being animated.

        Returns:
            int: Number of active packet animations.
        """

        return len(self.packet_items)
