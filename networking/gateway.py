from networking.packet import Packet


class Gateway:
    def __init__(self, device_id, ip_address, queue_limit=20):
        self.device_id = device_id
        self.ip_address = ip_address
        self.status = "ACTIVE"
        self.packet_queue = []
        self.server = None
        self.queue_limit = max(1, int(queue_limit))

    def set_server(self, server):
        self.server = server

    def set_queue_limit(self, limit):
        limit = int(limit)
        if limit < 1:
            raise ValueError("Gateway queue limit must be at least 1.")
        self.queue_limit = limit

    def get_queue_limit(self):
        return self.queue_limit

    def receive(self, packet):
        if not self.is_available() or not self.validate_packet(packet):
            return False
        return self.queue_packet(packet)

    def validate_packet(self, packet):
        return (packet is not None and packet.source is not None and
                packet.destination == self.device_id and packet.data is not None)

    def queue_packet(self, packet):
        if len(self.packet_queue) >= self.queue_limit:
            return False
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
    gateway = Gateway("GW-01", "192.168.1.1", queue_limit=2)
    print("Gateway queue limit:", gateway.get_queue_limit())
