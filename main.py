from config.config import *

# from devices.device import DeviceManager
from devices.sensor import Sensor, SensorManager
from devices.data_generator import DataGenerator

from networking.packet import Packet
from networking.transmission import Transmission
from networking.packet_loss import PacketLoss
from networking.gateway import Gateway
from networking.server import Server


class IoTNetworkSimulator:

    def __init__(self):
        self.running = False
        self.simulation_time = 0

        # self.device_manager = DeviceManager()
        self.sensor_manager = SensorManager()

        self.data_generator = DataGenerator()

        self.transmission = Transmission(
            BASE_DELAY,
            DELAY_VARIATION
        )

        self.packet_loss = PacketLoss(
            PACKET_LOSS_PROBABILITY
        )

        self.gateway = None
        self.server = None

        self.packet_counter = 0

        self.initialize()

    def initialize(self):
        self.create_devices()
        self.create_sensors()

    def create_devices(self):
        self.gateway = Gateway(
            "GW-01",
            NETWORK_PREFIX + "1"
        )

        self.server = Server(
            "SERVER-01",
            NETWORK_PREFIX + "100"
        )
        self.gateway.set_server(self.server)

    def create_sensors(self):

        sensor1 = Sensor("S-01", "temperature", DEFAULT_SENSOR_INTERVAL)
        sensor2 = Sensor("S-02", "humidity", DEFAULT_SENSOR_INTERVAL)
        sensor3 = Sensor("S-03", "light", DEFAULT_SENSOR_INTERVAL)

        sensor1.activate()
        sensor2.activate()
        sensor3.activate()

        self.sensor_manager.add_sensor(sensor1)
        self.sensor_manager.add_sensor(sensor2)
        self.sensor_manager.add_sensor(sensor3)

    def start_simulation(self):
        self.running = True
        print("Simulation started.")

        self.update_simulation()

    def pause_simulation(self):
        self.running = False
        print("Simulation paused.")

    def reset_simulation(self):
        self.running = False
        self.simulation_time = 0
        self.packet_counter = 0

        self.sensor_manager = SensorManager()

        self.initialize()

        print("Simulation reset.")

    def update_simulation(self):
        if not self.running:
            return

        self.process_sensor_events()
        self.process_network()
        self.update_metrics()
        self.update_gui()

    def process_sensor_events(self):

        sensors = self.sensor_manager.get_all_sensors()

        print("Number of sensors:", len(sensors))

        for sensor in sensors:

            print(
                "Sensor:",
                sensor.device_id,
                "Status:",
                sensor.get_status()
            )

            if sensor.get_status() != "ACTIVE":
                continue

            reading = self.data_generator.generate_reading(
                sensor.sensor_type
            )

            self.packet_counter += 1

            packet = Packet(
                f"P-{self.packet_counter}",
                sensor.device_id,
                self.gateway.device_id,
                reading
            )

            print(
                f"{sensor.device_id} generated "
                f"packet {packet.packet_id}: {reading}"
            )

            self.transmission.transmit(
                packet,
                sensor,
                self.gateway
            )

            if self.packet_loss.is_packet_lost():
                packet.update_status("LOST")
                print(f"Packet {packet.packet_id} was lost.")
                continue

            self.gateway.receive(packet)

    def process_network(self):

        self.gateway.process_queue()

        print(
            "Gateway queue size:",
            self.gateway.get_queue_size()
        )

        print(
            "Server packet count:",
            self.server.get_packet_count()
        )

    def update_metrics(self):
        # Metrics will be added later
        pass

    def update_gui(self):
        # Dashboard will be added later
        pass

    def run(self):
        self.start_simulation()


def main():
    simulator = IoTNetworkSimulator()
    simulator.run()


if __name__ == "__main__":
    main()