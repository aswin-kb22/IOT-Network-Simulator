from networking.packet import Packet


def test_create_packet():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    assert packet is not None
    assert packet.packet_id == "P-01"


def test_packet_metadata():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    assert packet.packet_id == "P-01"
    assert packet.source == "S-01"
    assert packet.destination == "GW-01"
    assert packet.data == {"temperature": 25}


def test_packet_status():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    assert packet.get_status() == "QUEUED"


def test_packet_timestamp():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    packet.set_timestamp("CREATED")

    assert "CREATED" in packet.timestamps
    assert packet.timestamps["CREATED"] is not None


def test_packet_status_update():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    packet.update_status("TRANSMITTING")

    assert packet.get_status() == "TRANSMITTING"

    packet.update_status("DELIVERED")

    assert packet.get_status() == "DELIVERED"


def test_packet_info():
    packet = Packet(
        "P-01",
        "S-01",
        "GW-01",
        {"temperature": 25}
    )

    info = packet.get_info()

    assert info["packet_id"] == "P-01"
    assert info["source"] == "S-01"
    assert info["destination"] == "GW-01"
    assert info["data"] == {"temperature": 25}
    assert info["status"] == "QUEUED"
    assert "timestamps" in info