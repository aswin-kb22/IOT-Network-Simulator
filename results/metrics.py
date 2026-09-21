import time


class Metrics:

    def __init__(self):
        self.packets_generated = 0
        self.packets_forwarded = 0
        self.packets_delivered = 0
        self.packets_lost = 0

        self.delays = []
        self.queue_pressures = []
        self.events = []

    def record_packet_generated(self, packet):
        self.packets_generated += 1

        self.record_event(
            f"Packet {packet.packet_id} generated"
        )

    def record_packet_forwarded(self, packet):
        self.packets_forwarded += 1

        self.record_event(
            f"Packet {packet.packet_id} forwarded"
        )

    def record_packet_delivered(self, packet):
        self.packets_delivered += 1

        # Calculate end-to-end delay if timestamps are available
        timestamps = packet.timestamps

        if "created" in timestamps:
            delivery_time = timestamps.get(
                "delivered",
                time.time()
            )

            delay = delivery_time - timestamps["created"]

            if delay >= 0:
                self.delays.append(delay)

        self.record_event(
            f"Packet {packet.packet_id} delivered"
        )

    def record_packet_lost(self, packet):
        self.packets_lost += 1

        self.record_event(
            f"Packet {packet.packet_id} lost"
        )

    def calculate_packet_loss(self):
        total_packets = (
            self.packets_delivered +
            self.packets_lost
        )

        if total_packets == 0:
            return 0.0

        return (
            self.packets_lost /
            total_packets
        ) * 100

    def calculate_average_delay(self):
        if not self.delays:
            return 0.0

        return sum(self.delays) / len(self.delays)

    def calculate_delivery_rate(self):
        total_packets = (
            self.packets_delivered +
            self.packets_lost
        )

        if total_packets == 0:
            return 0.0

        return (
            self.packets_delivered /
            total_packets
        ) * 100

    def calculate_throughput(self, simulation_time):
        if simulation_time <= 0:
            return 0.0

        return (
            self.packets_delivered /
            simulation_time
        )

    def calculate_queue_pressure(self, queue_size):
        self.queue_pressures.append(queue_size)

        return queue_size

    def get_summary(self):
        return {
            "packets_generated": self.packets_generated,
            "packets_forwarded": self.packets_forwarded,
            "packets_delivered": self.packets_delivered,
            "packets_lost": self.packets_lost,
            "packet_loss_percentage":
                self.calculate_packet_loss(),
            "average_delay":
                self.calculate_average_delay(),
            "delivery_rate":
                self.calculate_delivery_rate(),
            "queue_pressure":
                self.queue_pressures[-1]
                if self.queue_pressures
                else 0
        }

    def record_event(self, event):
        self.events.append({
            "event": event,
            "timestamp": time.time()
        })

    def reset(self):
        self.packets_generated = 0
        self.packets_forwarded = 0
        self.packets_delivered = 0
        self.packets_lost = 0

        self.delays.clear()
        self.queue_pressures.clear()
        self.events.clear()

if __name__ == "__main__":

    from networking.packet import Packet

    metrics = Metrics()

    packet1 = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    packet2 = Packet(
        "P-02",
        "S-02",
        "GW-01",
        {"humidity": 60}
    )

    packet3 = Packet(
        "P-03",
        "S-03",
        "GW-01",
        {"light": 500}
    )

    # Record generated packets
    metrics.record_packet_generated(packet1)
    metrics.record_packet_generated(packet2)
    metrics.record_packet_generated(packet3)

    # Forward two packets
    metrics.record_packet_forwarded(packet1)
    metrics.record_packet_forwarded(packet2)

    # Deliver packet 1 and 2
    packet1.set_timestamp("created")
    packet1.set_timestamp("delivered")

    packet2.set_timestamp("created")
    packet2.set_timestamp("delivered")

    metrics.record_packet_delivered(packet1)
    metrics.record_packet_delivered(packet2)

    # Packet 3 is lost
    metrics.record_packet_lost(packet3)

    # Queue pressure
    metrics.calculate_queue_pressure(3)

    print("\n===== METRICS =====")

    summary = metrics.get_summary()

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nEvents:")

    for event in metrics.events:
        print(event)