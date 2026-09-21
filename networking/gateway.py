from networking.packet import Packet

class Gateway:

    def __init__(self, device_id, ip_address):
        self.device_id = device_id
        self.ip_address = ip_address
        self.status = "ACTIVE"
        self.packet_queue = []
        self.server = None

    def set_server(self, server):
        self.server = server

    def receive(self, packet):
        if not self.is_available():
            return False

        if not self.validate_packet(packet):
            return False

        return self.queue_packet(packet)

    def validate_packet(self, packet):
        if packet is None:
            return False

        if packet.source is None:
            return False

        if packet.destination != self.device_id:
            return False

        if packet.data is None:
            return False

        return True

    def queue_packet(self, packet):
        self.packet_queue.append(packet)
        packet.update_status("QUEUED")
        return True

    def process_queue(self):
        while self.packet_queue:
            packet = self.packet_queue.pop(0)
            self.forward_packet(packet)

    def forward_packet(self, packet):

        if self.server is None:
            return False

        packet.destination = self.server.device_id
        packet.update_status("TRANSMITTING")

        return self.server.receive(packet)

    def get_queue_size(self):
        return len(self.packet_queue)

    def is_available(self):
        return self.status == "ACTIVE"

    def clear_queue(self):
        self.packet_queue.clear()

if __name__ == "__main__":

    gateway = Gateway(
        "GW-01",
        "192.168.1.1"
    )

    packet1 = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 26.5}
    )

    packet2 = Packet(
        "P-02",
        "S-02",
        "GW-01",
        {"humidity": 55}
    )

    print("Gateway available:",
          gateway.is_available())

    print("\nReceiving packet 1:")
    print(gateway.receive(packet1))

    print("Queue size:",
          gateway.get_queue_size())

    print("\nReceiving packet 2:")
    print(gateway.receive(packet2))

    print("Queue size:",
          gateway.get_queue_size())

    print("\nProcessing queue:")

    gateway.process_queue()

    print("Queue size:",
          gateway.get_queue_size())

    print("Packet 1 status:",
          packet1.get_status())

    print("Packet 2 status:",
          packet2.get_status())

    gateway.clear_queue()

    print("\nAfter clearing queue:")
    print("Queue size:",
          gateway.get_queue_size())