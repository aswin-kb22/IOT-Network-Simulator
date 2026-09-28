import random


class PacketLoss:

    def __init__(self, loss_probability):
        self.loss_probability = loss_probability

    def is_packet_lost(self):
        return random.random() < self.loss_probability

    def apply_loss(self, packet):
        if self.is_packet_lost():
            packet.update_status("LOST")
            return False
        return True

    def get_loss_probability(self):
        return self.loss_probability

if __name__ == "__main__":

    packet_loss = PacketLoss(0.5)

    print("Packet loss probability:",
          packet_loss.get_loss_probability())

    print("\nTesting 20 packets:\n")

    lost = 0

    for i in range(20):

        if packet_loss.is_packet_lost():
            print(f"Packet {i + 1}: LOST")
            lost += 1
        else:
            print(f"Packet {i + 1}: DELIVERED")

    print("\nTotal lost:", lost)
    print("Total tested:", 20)