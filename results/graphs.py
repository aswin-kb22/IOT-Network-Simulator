import matplotlib.pyplot as plt


class GraphGenerator:

    def __init__(self, metrics):
        self.metrics = metrics

    # ---------------------------------------------------------
    # Packet statistics
    # ---------------------------------------------------------

    def plot_packet_statistics(self):
        """
        Plot generated, forwarded, delivered and lost packets.
        """

        data = self.metrics.get_summary()

        labels = [
            "Generated",
            "Forwarded",
            "Delivered",
            "Lost"
        ]

        values = [
            data.get("packets_generated", 0),
            data.get("packets_forwarded", 0),
            data.get("packets_delivered", 0),
            data.get("packets_lost", 0)
        ]

        figure, axis = plt.subplots()

        axis.bar(labels, values)

        axis.set_title("Packet Statistics")
        axis.set_xlabel("Packet Type")
        axis.set_ylabel("Number of Packets")

        figure.tight_layout()

        return figure

    # ---------------------------------------------------------
    # Packet loss
    # ---------------------------------------------------------

    def plot_packet_loss(self):
        """
        Plot packet loss percentage.
        """

        data = self.metrics.get_summary()

        loss = data.get(
            "packet_loss_percentage",
            0
        )

        labels = [
            "Delivered",
            "Lost"
        ]

        delivered = data.get(
            "packets_delivered",
            0
        )

        lost = data.get(
            "packets_lost",
            0
        )

        values = [
            delivered,
            lost
        ]

        figure, axis = plt.subplots()

        axis.bar(labels, values)

        axis.set_title(
            f"Packet Loss: {loss:.2f}%"
        )

        axis.set_xlabel("Packet Status")
        axis.set_ylabel("Number of Packets")

        figure.tight_layout()

        return figure

    # ---------------------------------------------------------
    # Delay
    # ---------------------------------------------------------

    def plot_delay(self):
        """
        Plot average packet delay.
        """

        data = self.metrics.get_summary()

        average_delay = data.get(
            "average_delay",
            0
        )

        figure, axis = plt.subplots()

        axis.bar(
            ["Average Delay"],
            [average_delay]
        )

        axis.set_title("Average Packet Delay")
        axis.set_ylabel("Delay (seconds)")

        figure.tight_layout()

        return figure

    # ---------------------------------------------------------
    # Delivery rate
    # ---------------------------------------------------------

    def plot_delivery_rate(self):
        """
        Plot packet delivery rate.
        """

        data = self.metrics.get_summary()

        delivery_rate = data.get(
            "delivery_rate",
            0
        )

        figure, axis = plt.subplots()

        axis.bar(
            ["Delivery Rate"],
            [delivery_rate]
        )

        axis.set_title("Packet Delivery Rate")
        axis.set_ylabel("Rate (%)")

        axis.set_ylim(
            0,
            100
        )

        figure.tight_layout()

        return figure

    # ---------------------------------------------------------
    # Throughput
    # ---------------------------------------------------------

    def plot_throughput(self):
        """
        Plot packet throughput.

        Throughput requires simulation time.
        """

        simulation_time = getattr(
            self.metrics,
            "simulation_time",
            0
        )

        if simulation_time <= 0:
            throughput = 0

        else:
            throughput = (
                self.metrics.packets_delivered
                / simulation_time
            )

        figure, axis = plt.subplots()

        axis.bar(
            ["Throughput"],
            [throughput]
        )

        axis.set_title("Packet Throughput")
        axis.set_ylabel("Packets / Second")

        figure.tight_layout()

        return figure

    # ---------------------------------------------------------
    # Save graph
    # ---------------------------------------------------------

    def save_graph(self, figure, filename):
        """
        Save a generated graph to a file.

        Parameters:
            figure: Matplotlib figure.
            filename: Output file path.
        """

        if figure is None:
            raise ValueError(
                "Figure cannot be None."
            )

        figure.savefig(
            filename,
            bbox_inches="tight"
        )