from datetime import datetime

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

        # =====================================================
        # Simulation state
        # =====================================================

        self.running = False
        self.simulation_time = 0
        self.simulation_speed = 1.0

        # =====================================================
        # Managers / modules
        # =====================================================

        self.sensor_manager = SensorManager()

        self.data_generator = DataGenerator()

        self.transmission = Transmission(
            BASE_DELAY,
            DELAY_VARIATION
        )

        self.packet_loss = PacketLoss(
            PACKET_LOSS_PROBABILITY
        )

        self.gateway_queue_limit = GATEWAY_QUEUE_LIMIT

        self.metrics = Metrics()

        # Dashboard will be connected in main()
        self.dashboard = None

        # =====================================================
        # Network devices
        # =====================================================

        self.gateway = None
        self.server = None

        # =====================================================
        # Packet tracking
        # =====================================================

        self.packet_counter = 0

        # Packets whose delivery has already been
        # recorded by Metrics
        self.processed_deliveries = set()

        # =====================================================
        # Initialize simulation
        # =====================================================

        self.initialize()

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def initialize(self):

        self.create_devices()
        # self.create_sensors()

    # =========================================================
    # CREATE NETWORK DEVICES
    # =========================================================

    def create_devices(self):

        self.gateway = Gateway(
            "GW-01",
            NETWORK_PREFIX + "1",
            queue_limit=self.gateway_queue_limit
        )

        self.server = Server(
            "SERVER-01",
            NETWORK_PREFIX + "100"
        )

        # Connect gateway to server
        self.gateway.set_server(
            self.server
        )


    def apply_network_conditions(self, loss_percent, base_delay_ms, variation_ms, queue_limit):
        """Apply live network settings from the dashboard."""
        loss_percent = float(loss_percent)
        base_delay_ms = float(base_delay_ms)
        variation_ms = float(variation_ms)
        queue_limit = int(queue_limit)
        if not 0 <= loss_percent <= 100:
            raise ValueError("Packet loss must be between 0 and 100%.")
        if base_delay_ms < 0 or variation_ms < 0:
            raise ValueError("Delay values cannot be negative.")
        if queue_limit < 1:
            raise ValueError("Queue limit must be at least 1.")
        self.packet_loss.set_loss_probability(loss_percent / 100.0)
        self.transmission.set_parameters(base_delay_ms / 1000.0, variation_ms / 1000.0)
        self.gateway_queue_limit = queue_limit
        if self.gateway is not None:
            self.gateway.set_queue_limit(queue_limit)
        if self.dashboard is not None:
            self.dashboard.update_activity({"event": f"Network settings updated: loss={loss_percent:g}%, delay={base_delay_ms:g}±{variation_ms:g} ms, queue={queue_limit}"})

    def add_sensor(self, sensor_type, interval=2):
        """Create and register a new sensor dynamically."""

        sensor_type = sensor_type.strip().lower()

        valid_types = {
            "temperature",
            "humidity",
            "light",
            "motion",
            "soil_moisture"
        }

        if sensor_type not in valid_types:
            raise ValueError("Unsupported sensor type.")

        if interval <= 0:
            raise ValueError("Sampling interval must be positive.")

        sensors = self.sensor_manager.get_all_sensors()

        # Generate the next available sensor ID.
        existing_ids = {sensor.device_id for sensor in sensors}

        number = 1
        while f"S-{number:02d}" in existing_ids:
            number += 1

        device_id = f"S-{number:02d}"

        # Assign an IP address based on the sensor number.
        ip_address = f"{NETWORK_PREFIX}{number + 10}"

        sensor = Sensor(
            device_id,
            sensor_type,
            interval
        )

        sensor.activate()

        self.sensor_manager.add_sensor(sensor)

        # Update the dashboard topology immediately.
        if self.dashboard is not None:
            if getattr(self.dashboard, "topology", None) is not None:
                self.dashboard.topology.add_sensor_node(sensor)
                self.dashboard.topology.connect_nodes(
                    sensor.device_id,
                    self.gateway.device_id
                )

        print(f"Added sensor {device_id} ({sensor_type})")

        return sensor


    def remove_sensor(self, device_id):
        """Remove a sensor from the simulator."""

        sensor = self.sensor_manager.get_sensor(device_id)

        if sensor is None:
            return False

        self.sensor_manager.remove_sensor(device_id)

        if self.dashboard is not None:
            if getattr(self.dashboard, "topology", None) is not None:
                self.dashboard.topology.remove_node(device_id)

        print(f"Removed sensor {device_id}")

        return True


    def _log_packet_event(self, packet, source, destination, event):
        """Add a timestamped packet event to the dashboard activity panel."""
        if self.dashboard is None:
            return

        dashboard_logger = getattr(self.dashboard, "update_activity", None)
        if not callable(dashboard_logger):
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"{timestamp}  {packet.packet_id}  {source} -> {destination}  {event}"
        try:
            dashboard_logger(message)
        except Exception as error:
            print(f"Activity log update error ({event}): {error}")

    def _record_link_event(self, source, destination, event):
        """Update a topology link counter when the dashboard is available."""
        topology = getattr(self.dashboard, "topology", None) if self.dashboard else None
        if topology is not None:
            try:
                topology.record_connection_event(source, destination, event)
            except Exception as error:
                print(f"Connection counter update error ({event}): {error}")

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

        if self.running:
            return

        self.running = True

        print(
            "Simulation started."
        )

        self.update_simulation()

    # =========================================================
    # PAUSE SIMULATION
    # =========================================================

    def pause_simulation(self):

        self.running = False

        print(
            "Simulation paused."
        )

    # =========================================================
    # RESET SIMULATION
    # =========================================================

    def reset_simulation(self):

        self.running = False

        # Reset simulation time
        self.simulation_time = 0

        # Reset packet counter
        self.packet_counter = 0

        # Clear delivery tracking
        self.processed_deliveries.clear()

        # Reset metrics
        self.metrics.reset()

        # Clear dashboard animations
        if self.dashboard is not None:

            try:

                if self.dashboard.animation is not None:

                    self.dashboard.animation.clear_animations()

            except Exception as error:

                print(
                    "Animation reset error:",
                    error
                )

        # Recreate sensors
        self.sensor_manager = SensorManager()

        # Recreate complete network
        self.gateway = None
        self.server = None

        self.initialize()

        print(
            "Simulation reset."
        )

    # =========================================================
    # UPDATE SIMULATION
    # =========================================================

    def update_simulation(self):

        if not self.running:
            return

        # -----------------------------------------------------
        # Advance simulation time
        # -----------------------------------------------------

        self.simulation_time += 1

        self.metrics.simulation_time = (
            self.simulation_time
        )

        # -----------------------------------------------------
        # Process sensors
        # -----------------------------------------------------

        self.process_sensor_events()

        # -----------------------------------------------------
        # Process network
        # -----------------------------------------------------

        self.process_network()

        # -----------------------------------------------------
        # Update metrics
        # -----------------------------------------------------

        self.update_metrics()

        # -----------------------------------------------------
        # Update dashboard
        # -----------------------------------------------------

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

            # -------------------------------------------------
            # Ignore inactive sensors
            # -------------------------------------------------

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

            # -------------------------------------------------
            # Creation timestamp
            # -------------------------------------------------

            packet.set_timestamp(
                "created"
            )

            # -------------------------------------------------
            # Record generated packet
            # -------------------------------------------------

            self.metrics.record_packet_generated(packet)
            self._record_link_event(sensor.device_id, self.gateway.device_id, "sent")
            self._log_packet_event(packet, sensor.device_id, self.gateway.device_id, "SENT")

            print(
                f"{sensor.device_id} generated "
                f"packet {packet.packet_id}: "
                f"{reading}"
            )

            # -------------------------------------------------
            # START SENSOR → GATEWAY ANIMATION
            # -------------------------------------------------

            if self.dashboard is not None:

                try:

                    self.dashboard.animate_packet(
                        packet,
                        sensor.device_id,
                        self.gateway.device_id
                    )

                except Exception as error:

                    print(
                        "Sensor-to-gateway animation error:",
                        error
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

                self.metrics.record_packet_lost(packet)
                self._record_link_event(sensor.device_id, self.gateway.device_id, "lost")
                self._log_packet_event(packet, sensor.device_id, self.gateway.device_id, "LOST")
                self._log_packet_event(packet, sensor.device_id, self.gateway.device_id, "LOST")

                # Show lost packet on GUI
                if self.dashboard is not None:

                    try:

                        self.dashboard.update_packet_status(
                            packet.packet_id,
                            "lost"
                        )

                    except Exception as error:

                        print(
                            "Lost packet animation error:",
                            error
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

            if received:
                self._record_link_event(sensor.device_id, self.gateway.device_id, "received")
                self._log_packet_event(packet, sensor.device_id, self.gateway.device_id, "RECEIVED")

            if not received:

                packet.update_status(
                    "LOST"
                )

                self.metrics.record_packet_lost(packet)
                self._record_link_event(sensor.device_id, self.gateway.device_id, "lost")

                # Show rejected packet
                if self.dashboard is not None:

                    try:

                        self.dashboard.update_packet_status(
                            packet.packet_id,
                            "lost"
                        )

                    except Exception as error:

                        print(
                            "Gateway rejection animation error:",
                            error
                        )

                print(
                    f"Packet {packet.packet_id} "
                    f"was rejected by gateway."
                )

    # =========================================================
    # NETWORK PROCESSING
    # =========================================================

    def process_network(self):

        # -----------------------------------------------------
        # Save packets currently waiting in gateway
        # -----------------------------------------------------

        queued_packets = list(
            self.gateway.packet_queue
        )

        # -----------------------------------------------------
        # Record queue pressure
        # -----------------------------------------------------

        self.metrics.calculate_queue_pressure(
            self.gateway.get_queue_size()
        )

        # -----------------------------------------------------
        # Process gateway queue
        # -----------------------------------------------------

        self.gateway.process_queue()

        # -----------------------------------------------------
        # Record forwarded packets
        # -----------------------------------------------------

        for packet in queued_packets:

            self.metrics.record_packet_forwarded(packet)
            self._record_link_event(self.gateway.device_id, self.server.device_id, "forwarded")
            self._log_packet_event(packet, self.gateway.device_id, self.server.device_id, "FORWARDED")

            # -------------------------------------------------
            # GATEWAY → SERVER ANIMATION
            # -------------------------------------------------

            if self.dashboard is not None:

                try:

                    self.dashboard.animate_packet(
                        packet,
                        self.gateway.device_id,
                        self.server.device_id
                    )

                except Exception as error:

                    print(
                        "Gateway-to-server animation error:",
                        error
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

                # -------------------------------------------------
                # Delivery timestamp
                # -------------------------------------------------

                packet.set_timestamp(
                    "delivered"
                )

                # -------------------------------------------------
                # Record delivery
                # -------------------------------------------------

                self.metrics.record_packet_delivered(packet)
                self._record_link_event(self.gateway.device_id, self.server.device_id, "delivered")
                self._log_packet_event(packet, self.gateway.device_id, self.server.device_id, "DELIVERED")

                # -------------------------------------------------
                # Mark as processed
                # -------------------------------------------------

                self.processed_deliveries.add(
                    packet.packet_id
                )

                # -------------------------------------------------
                # Update animation
                # -------------------------------------------------

                if self.dashboard is not None:

                    try:

                        self.dashboard.update_packet_status(
                            packet.packet_id,
                            "delivered"
                        )

                    except Exception as error:

                        print(
                            "Delivery animation error:",
                            error
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

            summary = (
                self.metrics
                .get_summary()
            )

            # -------------------------------------------------
            # Throughput
            # -------------------------------------------------

            summary["throughput"] = (
                self.metrics
                .calculate_throughput(
                    self.simulation_time
                )
            )

            # -------------------------------------------------
            # Packet loss
            # -------------------------------------------------

            summary["packet_loss_rate"] = (
                summary.get(
                    "packet_loss_percentage",
                    0
                )
            )

            # -------------------------------------------------
            # Update statistics
            # -------------------------------------------------

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
                speed = 0.1

            self.simulation_speed = speed

            # Pass speed to animation as well
            if self.dashboard is not None:

                try:

                    if self.dashboard.animation is not None:

                        self.dashboard.animation.set_animation_speed(
                            speed
                        )

                except Exception as error:

                    print(
                        "Animation speed error:",
                        error
                    )

        except (
            ValueError,
            TypeError
        ):

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

    # Create simulator
    simulator = IoTNetworkSimulator()

    # Create dashboard
    dashboard = Dashboard(
        simulator
    )

    # Connect dashboard to simulator
    simulator.dashboard = dashboard

    # Start GUI
    dashboard.run()


# =============================================================
# ENTRY POINT
# =============================================================

if __name__ == "__main__":

    main()