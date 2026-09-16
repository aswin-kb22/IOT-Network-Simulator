class Packet:

    def __init__(self, packet_id, source, destination, data):
        self.packet_id = packet_id
        self.source = source
        self.destination = destination
        self.data = data

        self.status = "QUEUED"
        self.timestamps = {}

    def update_status(self, status):
        self.status = status

    def add_timestamp(self, event, timestamp):
        self.timestamps[event] = timestamp

    def get_status(self):
        return self.status

    def get_info(self):
        return {
            "packet_id": self.packet_id,
            "source": self.source,
            "destination": self.destination,
            "data": self.data,
            "status": self.status,
            "timestamps": self.timestamps
        }

    def set_timestamp(self, event):
        import time
        self.timestamps[event] = time.time()