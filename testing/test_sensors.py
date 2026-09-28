from devices.sensor import Sensor, SensorManager
from devices.data_generator import DataGenerator


def test_create_sensor():
    sensor = Sensor("S-01", "temperature", 2)

    assert sensor is not None
    assert sensor.device_id == "S-01"
    assert sensor.sensor_type == "temperature"


def test_sensor_activation():
    sensor = Sensor("S-01", "temperature", 2)

    sensor.activate()

    assert sensor.get_status() == "ACTIVE"


def test_sensor_deactivation():
    sensor = Sensor("S-01", "temperature", 2)

    sensor.deactivate()

    assert sensor.get_status() == "INACTIVE"


def test_sensor_configuration():
    sensor = Sensor("S-01", "temperature", 2)

    sensor.set_sensor_type("humidity")

    assert sensor.sensor_type == "humidity"


def test_sensor_interval():
    sensor = Sensor("S-01", "temperature", 2)

    sensor.set_interval(5)

    assert sensor.interval == 5


def test_add_sensor():
    manager = SensorManager()
    sensor = Sensor("S-01", "temperature", 2)

    manager.add_sensor(sensor)

    assert manager.get_sensor("S-01") is sensor
    assert len(manager.get_all_sensors()) == 1


def test_remove_sensor():
    manager = SensorManager()
    sensor = Sensor("S-01", "temperature", 2)

    manager.add_sensor(sensor)
    manager.remove_sensor("S-01")

    assert manager.get_sensor("S-01") is None
    assert len(manager.get_all_sensors()) == 0


def test_generate_reading():
    generator = DataGenerator()

    reading = generator.generate_reading("temperature")

    assert reading is not None