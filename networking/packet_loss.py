import random


class PacketLoss:
    def __init__(self, loss_probability):
        self.set_loss_probability(loss_probability)

    def set_loss_probability(self, probability):
        probability = float(probability)
        if not 0.0 <= probability <= 1.0:
            raise ValueError("Loss probability must be between 0 and 1.")
        self.loss_probability = probability

    def is_packet_lost(self):
        return random.random() < self.loss_probability

    def apply_loss(self, packet):
        if self.is_packet_lost():
            packet.update_status("LOST")
            return False
        return True

    def get_loss_probability(self):
        return self.loss_probability
