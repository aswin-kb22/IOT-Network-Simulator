class Sensor:
    def __init__(self, device_id, sensor_type, interval=2):
        self.device_id = device_id
        self.sensor_type = sensor_type
        self.interval = interval
        self.status = "inactive"

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def set_interval(self, interval):
        if interval <= 0:
            raise ValueError("Interval must be greater than 0.")
        self.interval = interval

    def set_sensor_type(self, sensor_type):
        self.sensor_type = sensor_type

    def get_status(self):
        return self.status

    def get_info(self):
        return {
            "device_id": self.device_id,
            "sensor_type": self.sensor_type,
            "interval": self.interval,
            "status": self.status
        }


class SensorManager:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        if self.get_sensor(sensor.device_id) is not None:
            raise ValueError(f"Sensor with ID {sensor.device_id} already exists.")
        self.sensors.append(sensor)

    def remove_sensor(self, device_id):
        sensor = self.get_sensor(device_id)

        if sensor is None:
            return False

        self.sensors.remove(sensor)
        return True

    def get_sensor(self, device_id):
        for sensor in self.sensors:
            if sensor.device_id == device_id:
                return sensor
        return None

    def get_all_sensors(self):
        return self.sensors