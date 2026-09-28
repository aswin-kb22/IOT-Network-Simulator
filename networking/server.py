from networking.packet import Packet

class Server:

    def __init__(self, device_id, ip_address):
        self.device_id = device_id
        self.ip_address = ip_address
        self.status = "ACTIVE"
        self.received_packets = []

    def receive(self, packet):
        if self.status != "ACTIVE":
            return False

        if packet is None:
            return False

        return self.process_packet(packet)

    def process_packet(self, packet):
        if packet.destination != self.device_id:
            return False

        packet.update_status("DELIVERED")
        return self.store_packet(packet)

    def store_packet(self, packet):
        self.received_packets.append(packet)
        return True

    def get_received_packets(self):
        return self.received_packets

    def get_packet_count(self):
        return len(self.received_packets)

if __name__ == "__main__":

    server = Server(
        "SERVER-01",
        "192.168.1.100"
    )

    packet1 = Packet(
        "P-01",
        "GW-01",
        "SERVER-01",
        {"temperature": 26.5}
    )

    packet2 = Packet(
        "P-02",
        "GW-01",
        "SERVER-01",
        {"humidity": 55}
    )

    print("Initial packet count:",
          server.get_packet_count())

    print("\nReceiving packet 1:")
    print(server.receive(packet1))

    print("Packet status:",
          packet1.get_status())

    print("\nReceiving packet 2:")
    print(server.receive(packet2))

    print("Packet status:",
          packet2.get_status())

    print("\nFinal packet count:",
          server.get_packet_count())

    print("\nReceived packets:")

    for packet in server.get_received_packets():
        print(packet.get_info())