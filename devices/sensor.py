class Sensor:
    def __init__(self, device_id, sensor_type, interval=2):
        ...

    def activate(self):
        ...

    def deactivate(self):
        ...

    def set_interval(self, interval):
        ...

    def set_sensor_type(self, sensor_type):
        ...

    def get_status(self):
        ...

    def get_info(self):
        ...


class SensorManager:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        ...

    def remove_sensor(self, device_id):
        ...

    def get_sensor(self, device_id):
        ...

    def get_all_sensors(self):
        ...