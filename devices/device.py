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

if __name__ == "__main__":

    device = Device(
        "D-01",
        "192.168.1.10",
        "SENSOR"
    )

    print("Device ID:", device.get_device_id())
    print("IP Address:", device.get_ip())
    print("Status:", device.get_status())
    print("Info:", device.get_info())

    device.deactivate()

    print("\nAfter deactivation:")
    print("Status:", device.get_status())

    device.activate()

    print("\nAfter activation:")
    print("Status:", device.get_status())