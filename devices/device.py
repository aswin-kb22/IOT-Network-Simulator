class Device:

    def __init__(self, device_id, ip_address, device_type):
        self.device_id = device_id
        self.ip_address = ip_address
        self.device_type = device_type
        self.status = "ACTIVE"

    def activate(self):
        self.status = "ACTIVE"

    def deactivate(self):
        self.status = "INACTIVE"

    def set_ip(self, ip_address):
        self.ip_address = ip_address

    def get_ip(self):
        return self.ip_address

    def get_device_id(self):
        return self.device_id

    def get_status(self):
        return self.status

    def get_info(self):
        return {
            "device_id": self.device_id,
            "ip_address": self.ip_address,
            "device_type": self.device_type,
            "status": self.status
        }