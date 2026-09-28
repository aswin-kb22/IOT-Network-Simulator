import tkinter as tk

from gui.topology import Topology
from devices.sensor import Sensor
from networking.gateway import Gateway
from networking.server import Server


def create_topology():

    root = tk.Tk()
    root.withdraw()

    canvas = tk.Canvas(
        root,
        width=900,
        height=500
    )

    canvas.pack()

    topology = Topology(canvas)

    return root, canvas, topology


def test_add_sensor_node():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    sensor.activate()

    result = topology.add_sensor_node(sensor)

    assert result == "S-01"
    assert "S-01" in topology.nodes
    assert topology.sensor_count == 1

    root.destroy()


def test_add_gateway_node():

    root, canvas, topology = create_topology()

    gateway = Gateway(
        "GW-01",
        "192.168.1.1"
    )

    result = topology.add_gateway_node(gateway)

    assert result == "GW-01"
    assert "GW-01" in topology.nodes

    root.destroy()


def test_add_server_node():

    root, canvas, topology = create_topology()

    server = Server(
        "SERVER-01",
        "192.168.1.100"
    )

    result = topology.add_server_node(server)

    assert result == "SERVER-01"
    assert "SERVER-01" in topology.nodes

    root.destroy()


def test_connect_nodes():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    gateway = Gateway(
        "GW-01",
        "192.168.1.1"
    )

    topology.add_sensor_node(sensor)
    topology.add_gateway_node(gateway)

    connection = topology.connect_nodes(
        sensor,
        gateway
    )

    assert connection == (
        "S-01",
        "GW-01"
    )

    assert len(topology.connections) == 1

    root.destroy()


def test_get_node_position():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    topology.add_sensor_node(sensor)

    position = topology.get_node_position(
        "S-01"
    )

    assert position is not None
    assert len(position) == 2

    root.destroy()


def test_get_node():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    topology.add_sensor_node(sensor)

    node = topology.get_node("S-01")

    assert node is not None
    assert node["type"] == "sensor"
    assert node["status"] == "ACTIVE"

    root.destroy()


def test_get_all_nodes():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    gateway = Gateway(
        "GW-01",
        "192.168.1.1"
    )

    topology.add_sensor_node(sensor)
    topology.add_gateway_node(gateway)

    nodes = topology.get_all_nodes()

    assert len(nodes) == 2
    assert "S-01" in nodes
    assert "GW-01" in nodes

    root.destroy()


def test_remove_node():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    topology.add_sensor_node(sensor)

    assert "S-01" in topology.nodes

    topology.remove_node("S-01")

    assert "S-01" not in topology.nodes
    assert topology.sensor_count == 0

    root.destroy()


def test_update_node_status():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    topology.add_sensor_node(sensor)

    topology.update_node_status(
        "S-01",
        "INACTIVE"
    )

    node = topology.get_node("S-01")

    assert node["status"] == "INACTIVE"

    root.destroy()


def test_clear_topology():

    root, canvas, topology = create_topology()

    sensor = Sensor(
        "S-01",
        "temperature",
        2
    )

    gateway = Gateway(
        "GW-01",
        "192.168.1.1"
    )

    server = Server(
        "SERVER-01",
        "192.168.1.100"
    )

    topology.add_sensor_node(sensor)
    topology.add_gateway_node(gateway)
    topology.add_server_node(server)

    topology.connect_nodes(
        sensor,
        gateway
    )

    topology.connect_nodes(
        gateway,
        server
    )

    topology.clear_topology()

    assert len(topology.nodes) == 0
    assert len(topology.connections) == 0
    assert topology.sensor_count == 0

    root.destroy()