from config.config import *

from devices.device import DeviceManager
from devices.sensor import Sensor, SensorManager
from devices.data_generator import DataGenerator

from networking.packet import Packet
from networking.transmission import Transmission
from networking.packet_loss import PacketLoss
from networking.gateway import Gateway
from networking.server import Server

from results.metrics import Metrics

from gui.dashboard import Dashboard

from gui.topology import Topology
from gui.animation import PacketAnimation


class IoTNetworkSimulator:

    def __init__(self):
        ...

    def initialize(self):
        ...

    def create_devices(self):
        ...

    def create_sensors(self):
        ...

    def start_simulation(self):
        ...

    def pause_simulation(self):
        ...

    def reset_simulation(self):
        ...

    def update_simulation(self):
        ...

    def process_sensor_events(self):
        ...

    def process_network(self):
        ...

    def update_metrics(self):
        ...

    def update_gui(self):
        ...

    def run(self):
        ...


def main():
    ...
