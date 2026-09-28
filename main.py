from config.config import *

from devices.sensor import Sensor, SensorManager
from devices.data_generator import DataGenerator

from networking.packet import Packet
from networking.transmission import Transmission
from networking.packet_loss import PacketLoss
from networking.gateway import Gateway
from networking.server import Server
from gui.dashboard import Dashboard

from results.metrics import Metrics


class IoTNetworkSimulator:

    def __init__(self):

        # -----------------------------------------------------
        # Simulation state
        # -----------------------------------------------------

        self.running = False
        self.simulation_time = 0

        # -----------------------------------------------------
        # Managers / modules
        # -----------------------------------------------------

        self.sensor_manager = SensorManager()
        self.data_generator = DataGenerator()

        self.transmission = Transmission(
            BASE_DELAY,
            DELAY_VARIATION
        )

        self.packet_loss = PacketLoss(
            PACKET_LOSS_PROBABILITY
        )

        self.metrics = Metrics()

        # GUI will be connected later
        self.dashboard = None

        # -----------------------------------------------------
        # Network devices
        # -----------------------------------------------------

        self.gateway = None
        self.server = None

        # -----------------------------------------------------
        # Packet tracking
        # -----------------------------------------------------

        self.packet_counter = 0

        # Packets whose delivery has already
        # been recorded by Metrics
        self.processed_deliveries = set()

        # -----------------------------------------------------
        # Initialize simulation
        # -----------------------------------------------------

        self.initialize()

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def initialize(self):

        self.create_devices()
        self.create_sensors()

    # =========================================================
    # CREATE NETWORK DEVICES
    # =========================================================

    def create_devices(self):

        self.gateway = Gateway(
            "GW-01",
            NETWORK_PREFIX + "1"
        )

        self.server = Server(
            "SERVER-01",
            NETWORK_PREFIX + "100"
        )

        self.gateway.set_server(
            self.server
        )

    # =========================================================
    # CREATE SENSORS
    # =========================================================

    def create_sensors(self):

        sensor1 = Sensor(
            "S-01",
            "temperature",
            DEFAULT_SENSOR_INTERVAL
        )

        sensor2 = Sensor(
            "S-02",
            "humidity",
            DEFAULT_SENSOR_INTERVAL
        )

        sensor3 = Sensor(
            "S-03",
            "light",
            DEFAULT_SENSOR_INTERVAL
        )

        # Activate sensors

        sensor1.activate()
        sensor2.activate()
        sensor3.activate()

        # Add sensors to manager

        self.sensor_manager.add_sensor(
            sensor1
        )

        self.sensor_manager.add_sensor(
            sensor2
        )

        self.sensor_manager.add_sensor(
            sensor3
        )

    # =========================================================
    # START SIMULATION
    # =========================================================

    def start_simulation(self):

        self.running = True

        print("Simulation started.")

        self.update_simulation()

    # =========================================================
    # PAUSE SIMULATION
    # =========================================================

    def pause_simulation(self):

        self.running = False

        print("Simulation paused.")

    # =========================================================
    # RESET SIMULATION
    # =========================================================

    def reset_simulation(self):

        self.running = False

        self.simulation_time = 0

        self.packet_counter = 0

        self.processed_deliveries.clear()

        # Reset metrics

        self.metrics.reset()

        # Recreate sensors

        self.sensor_manager = SensorManager()

        self.initialize()

        print("Simulation reset.")

    # =========================================================
    # UPDATE SIMULATION
    # =========================================================

    def update_simulation(self):

        if not self.running:
            return

        # Advance simulation time

        self.simulation_time += 1

        # Keep Metrics synchronized

        self.metrics.simulation_time = (
            self.simulation_time
        )

        # Process simulation

        self.process_sensor_events()

        self.process_network()

        self.update_metrics()

        self.update_gui()

    # =========================================================
    # SENSOR EVENTS
    # =========================================================

    def process_sensor_events(self):

        sensors = (
            self.sensor_manager
            .get_all_sensors()
        )

        print(
            "Number of sensors:",
            len(sensors)
        )

        for sensor in sensors:

            print(
                "Sensor:",
                sensor.device_id,
                "Status:",
                sensor.get_status()
            )

            # Ignore inactive sensors

            if sensor.get_status() != "ACTIVE":
                continue

            # -------------------------------------------------
            # Generate sensor reading
            # -------------------------------------------------

            reading = (
                self.data_generator
                .generate_reading(
                    sensor.sensor_type
                )
            )

            # -------------------------------------------------
            # Create packet
            # -------------------------------------------------

            self.packet_counter += 1

            packet = Packet(
                f"P-{self.packet_counter}",
                sensor.device_id,
                self.gateway.device_id,
                reading
            )

            # Record creation timestamp

            packet.set_timestamp(
                "created"
            )

            # Record generated packet

            self.metrics.record_packet_generated(
                packet
            )

            print(
                f"{sensor.device_id} generated "
                f"packet {packet.packet_id}: "
                f"{reading}"
            )

            # -------------------------------------------------
            # Transmission
            # -------------------------------------------------

            self.transmission.transmit(
                packet,
                sensor,
                self.gateway
            )

            # -------------------------------------------------
            # Packet loss
            # -------------------------------------------------

            if self.packet_loss.is_packet_lost():

                packet.update_status(
                    "LOST"
                )

                self.metrics.record_packet_lost(
                    packet
                )

                print(
                    f"Packet {packet.packet_id} "
                    f"was lost."
                )

                continue

            # -------------------------------------------------
            # Send packet to gateway
            # -------------------------------------------------

            received = self.gateway.receive(
                packet
            )

            if not received:

                packet.update_status(
                    "LOST"
                )

                self.metrics.record_packet_lost(
                    packet
                )

                print(
                    f"Packet {packet.packet_id} "
                    f"was rejected by gateway."
                )

    # =========================================================
    # NETWORK PROCESSING
    # =========================================================

    def process_network(self):

        # Save packets currently waiting
        # in gateway before processing

        queued_packets = list(
            self.gateway.packet_queue
        )

        # Record queue pressure

        self.metrics.calculate_queue_pressure(
            self.gateway.get_queue_size()
        )

        # Process gateway queue

        self.gateway.process_queue()

        # -----------------------------------------------------
        # Record forwarded packets
        # -----------------------------------------------------

        for packet in queued_packets:

            self.metrics.record_packet_forwarded(
                packet
            )

        # -----------------------------------------------------
        # Process delivered packets
        # -----------------------------------------------------

        received_packets = (
            self.server.get_received_packets()
        )

        for packet in received_packets:

            if (
                packet.packet_id
                not in self.processed_deliveries
            ):

                # Add delivery timestamp

                packet.set_timestamp(
                    "delivered"
                )

                # Record delivery

                self.metrics.record_packet_delivered(
                    packet
                )

                # Mark as processed

                self.processed_deliveries.add(
                    packet.packet_id
                )

        # -----------------------------------------------------
        # Console output
        # -----------------------------------------------------

        print(
            "Gateway queue size:",
            self.gateway.get_queue_size()
        )

        print(
            "Server packet count:",
            self.server.get_packet_count()
        )

    # =========================================================
    # UPDATE METRICS
    # =========================================================

    def update_metrics(self):

        # Metrics already records individual
        # packet events.

        # Synchronize simulation time.

        self.metrics.simulation_time = (
            self.simulation_time
        )

    # =========================================================
    # UPDATE GUI
    # =========================================================

    def update_gui(self):

        if self.dashboard is None:
            return

        try:

            summary = self.metrics.get_summary()

            # Add throughput because the current
            # Metrics.get_summary() does not include it.

            summary["throughput"] = (
                self.metrics.calculate_throughput(
                    self.simulation_time
                )
            )

            # Dashboard expects packet loss using
            # packet_loss_rate / packet_loss.

            summary["packet_loss_rate"] = (
                summary.get(
                    "packet_loss_percentage",
                    0
                )
            )

            self.dashboard.update_statistics(
                summary
            )

        except Exception as error:

            print(
                "Error updating GUI:",
                error
            )

    # =========================================================
    # GET SIMULATION TIME
    # =========================================================

    def get_simulation_time(self):

        return self.simulation_time

    # =========================================================
    # SET SIMULATION SPEED
    # =========================================================

    def set_simulation_speed(self, speed):

        try:

            speed = float(speed)

            if speed <= 0:
                return

            # Convert simulation speed into
            # animation/update delay.

            delay = int(
                100 / speed
            )

            if delay <= 0:
                delay = 1

            self.transmission.last_transmission_time = (
                self.transmission.last_transmission_time
            )

        except (ValueError, TypeError):

            pass

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        self.start_simulation()


# =============================================================
# MAIN
# =============================================================

def main():

    simulator = IoTNetworkSimulator()

    dashboard = Dashboard(simulator)

    simulator.dashboard = dashboard

    dashboard.run()


if __name__ == "__main__":
    main()