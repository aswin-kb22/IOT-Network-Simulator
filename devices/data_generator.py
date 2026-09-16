import random


class DataGenerator:
    """
    Generates synthetic sensor readings for the IoT Network Simulator.

    Supported sensor types:
        - temperature
        - humidity
        - light
        - motion
        - soil_moisture
    """

    def __init__(self):
        """
        Initialize the data generator with predefined
        ranges for different sensor types.
        """

        # Temperature in degree Celsius
        self.temperature_min = 20.0
        self.temperature_max = 35.0

        # Relative humidity in percentage
        self.humidity_min = 30.0
        self.humidity_max = 80.0

        # Light intensity in lux
        self.light_min = 0.0
        self.light_max = 1000.0

        # Soil moisture in percentage
        self.soil_moisture_min = 0.0
        self.soil_moisture_max = 100.0

        # Motion sensor values
        self.motion_values = [0, 1]

    def generate_temperature(self):
        """
        Generate a random temperature reading.

        Returns:
            float: Temperature value in degree Celsius.
        """

        temperature = random.uniform(
            self.temperature_min,
            self.temperature_max
        )

        return round(temperature, 2)

    def generate_humidity(self):
        """
        Generate a random humidity reading.

        Returns:
            float: Humidity percentage.
        """

        humidity = random.uniform(
            self.humidity_min,
            self.humidity_max
        )

        return round(humidity, 2)

    def generate_light(self):
        """
        Generate a random light-intensity reading.

        Returns:
            float: Light intensity in lux.
        """

        light = random.uniform(
            self.light_min,
            self.light_max
        )

        return round(light, 2)

    def generate_motion(self):
        """
        Generate a random motion sensor reading.

        Returns:
            int: 0 for no motion, 1 for motion detected.
        """

        return random.choice(self.motion_values)

    def generate_soil_moisture(self):
        """
        Generate a random soil-moisture reading.

        Returns:
            float: Soil moisture percentage.
        """

        soil_moisture = random.uniform(
            self.soil_moisture_min,
            self.soil_moisture_max
        )

        return round(soil_moisture, 2)

    def generate_reading(self, sensor_type):
        """
        Generate a reading based on the specified sensor type.

        Parameters:
            sensor_type (str): Type of sensor.

        Returns:
            int/float: Generated sensor reading.

        Raises:
            ValueError: If the sensor type is not supported.
        """

        if not isinstance(sensor_type, str):
            raise TypeError("sensor_type must be a string")

        sensor_type = sensor_type.lower().strip()

        if sensor_type == "temperature":
            return self.generate_temperature()

        elif sensor_type == "humidity":
            return self.generate_humidity()

        elif sensor_type == "light":
            return self.generate_light()

        elif sensor_type == "motion":
            return self.generate_motion()

        elif sensor_type in ["soil_moisture", "soil moisture"]:
            return self.generate_soil_moisture()

        else:
            raise ValueError(
                f"Unsupported sensor type: {sensor_type}"
            )
