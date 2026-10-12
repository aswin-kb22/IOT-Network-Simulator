import tkinter as tk


class PacketAnimation:

    def __init__(self, canvas):
        self.canvas = canvas

        # packet_id -> canvas item
        self.packet_items = {}

        # packet_id -> animation information
        self.animation_data = {}

        self.animation_speed = 1.0

        # Colors based on packet state
        self.status_colors = {
            "created": "#3498db",
            "queued": "#9b59b6",
            "transmitting": "#f39c12",
            "forwarded": "#f39c12",
            "delivered": "#2ecc71",
            "received": "#2ecc71",
            "lost": "#e74c3c",
            "dropped": "#e74c3c",
            "failed": "#e74c3c"
        }

    # =========================================================
    # ANIMATE PACKET
    # =========================================================

    def animate_packet(self, packet, source, destination, duration=None):

        packet_id = self._get_packet_id(packet)

        source_position = self._get_position(source)
        destination_position = self._get_position(destination)

        if source_position is None or destination_position is None:
            return

        # Remove old animation for same packet if necessary
        self.remove_packet(packet_id)

        x1, y1 = source_position
        x2, y2 = destination_position

        # Initial packet position
        radius = 8

        color = self.status_colors["transmitting"]

        item = self.canvas.create_oval(
            x1 - radius,
            y1 - radius,
            x1 + radius,
            y1 + radius,
            fill=color,
            outline="black",
            width=1
        )

        # Packet label
        label = self.canvas.create_text(
            x1,
            y1 - 16,
            text=str(packet_id),
            fill="black",
            font=("Arial", 8, "bold")
        )

        self.packet_items[packet_id] = {
            "circle": item,
            "label": label
        }

        # Store animation information
        self.animation_data[packet_id] = {
            "source": source_position,
            "destination": destination_position,
            "start_time": None,
            "duration": duration if duration else 1000,
            "progress": 0.0,
            "packet": packet,
            "status": "transmitting"
        }

        self._move_packet(packet_id)

    # =========================================================
    # MOVE PACKET
    # =========================================================

    def _move_packet(self, packet_id):

        if packet_id not in self.animation_data:
            return

        if packet_id not in self.packet_items:
            return

        data = self.animation_data[packet_id]

        source = data["source"]
        destination = data["destination"]

        # Increment progress
        speed = max(0.1, self.animation_speed)

        step = 0.025 * speed

        data["progress"] += step

        progress = min(
            data["progress"],
            1.0
        )

        x = (
            source[0]
            + (destination[0] - source[0]) * progress
        )

        y = (
            source[1]
            + (destination[1] - source[1]) * progress
        )

        items = self.packet_items[packet_id]

        circle = items["circle"]
        label = items["label"]

        radius = 8

        # Move circle
        self.canvas.coords(
            circle,
            x - radius,
            y - radius,
            x + radius,
            y + radius
        )

        # Move label
        self.canvas.coords(
            label,
            x,
            y - 16
        )

        # Continue animation
        if progress < 1.0:

            self.canvas.after(
                30,
                lambda: self._move_packet(packet_id)
            )

        else:

            # Reached destination
            self.update_packet_position(
                packet_id,
                destination
            )

            # Do NOT automatically mark delivered.
            # The simulation decides the actual packet state.

    # =========================================================
    # UPDATE POSITION
    # =========================================================

    def update_packet_position(self, packet_id, position):

        if packet_id not in self.packet_items:
            return

        x, y = position

        radius = 8

        items = self.packet_items[packet_id]

        self.canvas.coords(
            items["circle"],
            x - radius,
            y - radius,
            x + radius,
            y + radius
        )

        self.canvas.coords(
            items["label"],
            x,
            y - 16
        )

    # =========================================================
    # SHOW STATUS
    # =========================================================

    def show_packet_status(self, packet_id, status):

        if packet_id not in self.packet_items:
            return

        status = status.lower()

        color = self.status_colors.get(
            status,
            "#3498db"
        )

        circle = self.packet_items[packet_id]["circle"]

        self.canvas.itemconfig(
            circle,
            fill=color
        )

        if packet_id in self.animation_data:

            self.animation_data[
                packet_id
            ]["status"] = status

        # Lost packets
        if status in (
            "lost",
            "dropped",
            "failed"
        ):

            self._show_lost_packet(
                packet_id
            )

        # Delivered packets
        elif status in (
            "delivered",
            "received"
        ):

            self.canvas.itemconfig(
                circle,
                fill="#2ecc71"
            )

            self.canvas.after(
                500,
                lambda: self.remove_packet(packet_id)
            )

    # =========================================================
    # LOST PACKET EFFECT
    # =========================================================

    def _show_lost_packet(self, packet_id):

        if packet_id not in self.packet_items:
            return

        items = self.packet_items[packet_id]

        circle = items["circle"]

        self.canvas.itemconfig(
            circle,
            fill="#e74c3c",
            outline="#8b0000",
            width=2
        )

        # Make packet disappear after short delay
        self.canvas.after(
            700,
            lambda: self.remove_packet(packet_id)
        )

    # =========================================================
    # REMOVE PACKET
    # =========================================================

    def remove_packet(self, packet_id):

        if packet_id in self.packet_items:

            items = self.packet_items[packet_id]

            try:
                self.canvas.delete(
                    items["circle"]
                )

                self.canvas.delete(
                    items["label"]
                )

            except tk.TclError:
                pass

            del self.packet_items[packet_id]

        if packet_id in self.animation_data:
            del self.animation_data[packet_id]

    # =========================================================
    # CLEAR ALL
    # =========================================================

    def clear_animations(self):

        for packet_id in list(
            self.packet_items.keys()
        ):

            self.remove_packet(
                packet_id
            )

        self.packet_items.clear()
        self.animation_data.clear()

    # =========================================================
    # SPEED
    # =========================================================

    def set_animation_speed(self, speed):

        try:

            speed = float(speed)

            if speed <= 0:
                speed = 0.1

            self.animation_speed = speed

        except (
            ValueError,
            TypeError
        ):

            pass

    # =========================================================
    # ACTIVE PACKETS
    # =========================================================

    def get_active_packet_count(self):

        return len(
            self.packet_items
        )

    # =========================================================
    # PACKET ID
    # =========================================================

    def _get_packet_id(self, packet):

        if hasattr(packet, "packet_id"):
            return packet.packet_id

        if isinstance(packet, dict):
            return packet.get(
                "packet_id",
                "unknown"
            )

        return str(packet)

    # =========================================================
    # POSITION
    # =========================================================

    def _get_position(self, node):

        if node is None:
            return None

        # Tuple/list
        if isinstance(node, (tuple, list)):

            if len(node) >= 2:
                return (
                    float(node[0]),
                    float(node[1])
                )

        # Dictionary
        if isinstance(node, dict):

            if "x" in node and "y" in node:

                return (
                    float(node["x"]),
                    float(node["y"])
                )

        # Object with x/y
        if hasattr(node, "x") and hasattr(node, "y"):

            return (
                float(node.x),
                float(node.y)
            )

        return None