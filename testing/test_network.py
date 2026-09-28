from networking.packet import Packet
from networking.transmission import Transmission
from networking.packet_loss import PacketLoss
from networking.gateway import Gateway
from networking.server import Server


def test_transmission():
    transmission = Transmission(0.05, 0.01)

    delay = transmission.calculate_delay()

    assert 0.04 <= delay <= 0.06


def test_delay():
    transmission = Transmission(0.05, 0.01)

    delay1 = transmission.calculate_delay()
    delay2 = transmission.calculate_delay()

    assert 0.04 <= delay1 <= 0.06
    assert 0.04 <= delay2 <= 0.06


def test_packet_loss():
    packet_loss = PacketLoss(1.0)

    assert packet_loss.is_packet_lost() is True


def test_gateway_receive():
    gateway = Gateway("GW-01", "192.168.1.1")

    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    result = gateway.receive(packet)

    assert result is True
    assert gateway.get_queue_size() == 1


def test_gateway_queue():
    gateway = Gateway("GW-01", "192.168.1.1")

    packet1 = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    packet2 = Packet(
        "P-02",
        "S-02",
        "GW-01",
        {"humidity": 60}
    )

    gateway.receive(packet1)
    gateway.receive(packet2)

    assert gateway.get_queue_size() == 2

    gateway.clear_queue()

    assert gateway.get_queue_size() == 0


def test_gateway_forward():
    gateway = Gateway("GW-01", "192.168.1.1")

    server = Server(
        "SERVER-01",
        "192.168.1.100"
    )

    gateway.set_server(server)

    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    result = gateway.receive(packet)

    assert result is True
    assert gateway.get_queue_size() == 1

    gateway.process_queue()

    assert gateway.get_queue_size() == 0
    assert packet.get_status() == "DELIVERED"
    assert server.get_packet_count() == 1


def test_server_receive():
    server = Server("SERVER-01", "192.168.1.100")

    packet = Packet(
        "P-01",
        "GW-01",
        "SERVER-01",
        {"temperature": 25}
    )

    result = server.receive(packet)

    assert result is True
    assert packet.get_status() == "DELIVERED"
    assert server.get_packet_count() == 1


def test_end_to_end_delivery():
    gateway = Gateway("GW-01", "192.168.1.1")
    server = Server("SERVER-01", "192.168.1.100")

    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    # Sensor → Gateway
    assert gateway.receive(packet) is True

    # Gateway processing
    gateway.process_queue()

    # Gateway → Server
    packet.destination = "SERVER-01"
    assert server.receive(packet) is True

    # Verify final delivery
    assert packet.get_status() == "DELIVERED"
    assert server.get_packet_count() == 1