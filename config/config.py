# Simulation settings
SIMULATION_TIME = 60
SIMULATION_SPEED = 1.0

# Sensor settings
DEFAULT_SENSOR_INTERVAL = 2

# Network settings
BASE_DELAY = 0.05
DELAY_VARIATION = 0.01

# Packet loss
PACKET_LOSS_PROBABILITY = 0.10

# Gateway settings
GATEWAY_PROCESSING_TIME = 0.02
GATEWAY_QUEUE_LIMIT = 20

# Network addressing
NETWORK_PREFIX = "192.168.1."

if __name__ == "__main__":

    print("Simulation Time:", SIMULATION_TIME)
    print("Simulation Speed:", SIMULATION_SPEED)
    print("Sensor Interval:", DEFAULT_SENSOR_INTERVAL)
    print("Base Delay:", BASE_DELAY)
    print("Delay Variation:", DELAY_VARIATION)
    print("Packet Loss Probability:", PACKET_LOSS_PROBABILITY)
    print("Gateway Processing Time:", GATEWAY_PROCESSING_TIME)
    print("Gateway Queue Limit:", GATEWAY_QUEUE_LIMIT)
    print("Network Prefix:", NETWORK_PREFIX)