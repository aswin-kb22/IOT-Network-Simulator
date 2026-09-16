import random
import time


class Transmission:

    def __init__(self, base_delay, delay_variation):
        self.base_delay = base_delay
        self.delay_variation = delay_variation
        self.last_transmission_time = 0.0

    def calculate_delay(self):
        """
        Calculate a random transmission delay.

        Returns:
            float: Transmission delay in seconds.
        """

        minimum_delay = max(
            0.0,
            self.base_delay - self.delay_variation
        )

        maximum_delay = (
            self.base_delay + self.delay_variation
        )

        delay = random.uniform(
            minimum_delay,
            maximum_delay
        )

        return delay

    def transmit(self, packet, source, destination):
        """
        Simulate transmission of a packet
        from source to destination.

        Args:
            packet: Packet object.
            source: Source device.
            destination: Destination device.

        Returns:
            float: Transmission delay in seconds.
        """

        delay = self.calculate_delay()

        self.last_transmission_time = delay

        packet.update_status("TRANSMITTING")

        packet.add_timestamp(
            "transmission_start",
            time.time()
        )

        return delay

    def get_transmission_time(self):
        """
        Return the delay of the last transmission.

        Returns:
            float: Last transmission delay.
        """

        return self.last_transmission_time

    def get_delivery_time(self, start_time):
        """
        Calculate the expected packet delivery time.

        Args:
            start_time: Transmission start time.

        Returns:
            float: Expected delivery timestamp.
        """

        return start_time + self.last_transmission_time
