import matplotlib

matplotlib.use("Agg")

from results.metrics import Metrics
from results.graphs import GraphGenerator
from networking.packet import Packet


def create_metrics():

    metrics = Metrics()

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

    metrics.record_packet_generated(packet1)
    metrics.record_packet_generated(packet2)

    metrics.record_packet_forwarded(packet1)

    packet1.set_timestamp("created")
    packet1.set_timestamp("delivered")

    metrics.record_packet_delivered(packet1)
    metrics.record_packet_lost(packet2)

    metrics.simulation_time = 10

    return metrics


def test_graph_generator_creation():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    assert generator is not None


def test_packet_statistics_graph():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_packet_statistics()

    assert figure is not None


def test_packet_loss_graph():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_packet_loss()

    assert figure is not None


def test_delay_graph():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_delay()

    assert figure is not None


def test_delivery_rate_graph():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_delivery_rate()

    assert figure is not None


def test_throughput_graph():

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_throughput()

    assert figure is not None


def test_save_graph(tmp_path):

    metrics = create_metrics()

    generator = GraphGenerator(metrics)

    figure = generator.plot_packet_statistics()

    filename = tmp_path / "packet_statistics.png"

    generator.save_graph(
        figure,
        str(filename)
    )

    assert filename.exists()