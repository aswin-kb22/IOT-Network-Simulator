# testing/test_metrics.py
from results.metrics import Metrics
from networking.packet import Packet


def test_record_generated_and_lost():
    metrics = Metrics()
    packet = Packet("P-01", "S-01", "GW-01", {"temperature": 25})

    metrics.record_packet_generated(packet)
    metrics.record_packet_lost(packet)

    summary = metrics.get_summary()
    assert summary["packets_generated"] == 1
    assert summary["packets_lost"] == 1
    assert summary["packet_loss_percentage"] == 100.0


def test_record_delivered_computes_delay():
    metrics = Metrics()
    packet = Packet("P-01", "S-01", "GW-01", {"temperature": 25})

    packet.set_timestamp("created")
    packet.set_timestamp("delivered")

    metrics.record_packet_generated(packet)
    metrics.record_packet_forwarded(packet)
    metrics.record_packet_delivered(packet)

    summary = metrics.get_summary()
    assert summary["packets_delivered"] == 1
    assert summary["average_delay"] >= 0.0
    assert summary["delivery_rate"] == 100.0