class Gateway:

    def __init__(self, device_id, ip_address):
        self.device_id = device_id
        self.ip_address = ip_address
        self.status = "ACTIVE"
        self.packet_queue = []

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
        packet.update_status("TRANSMITTING")
        return packet

    def get_queue_size(self):
        return len(self.packet_queue)

    def is_available(self):
        return self.status == "ACTIVE"

    def clear_queue(self):
        self.packet_queue.clear()