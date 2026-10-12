import random
import time
from networking.packet import Packet


class Transmission:
    def __init__(self, base_delay, delay_variation):
        self.last_transmission_time = 0.0
        self.set_parameters(base_delay, delay_variation)

    def set_parameters(self, base_delay, delay_variation):
        base_delay, delay_variation = float(base_delay), float(delay_variation)
        if base_delay < 0 or delay_variation < 0:
            raise ValueError("Delay values cannot be negative.")
        self.base_delay = base_delay
        self.delay_variation = delay_variation

    def calculate_delay(self):
        minimum_delay = max(0.0, self.base_delay - self.delay_variation)
        return random.uniform(minimum_delay, self.base_delay + self.delay_variation)

    def transmit(self, packet, source, destination):
        delay = self.calculate_delay()
        self.last_transmission_time = delay
        packet.update_status("TRANSMITTING")
        packet.add_timestamp("transmission_start", time.time())
        return delay

    def get_transmission_time(self):
        return self.last_transmission_time

    def get_delivery_time(self, start_time):
        return start_time + self.last_transmission_time
