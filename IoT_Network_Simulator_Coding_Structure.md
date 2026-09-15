# IoT Network Simulator — Coding Project Structure

## Project Directory

```text
IoT-Network-Simulator/
│
├── main.py                    # Member 1 – Integration / entry point
│
├── config/
│   └── config.py              # Simulation settings
│
├── devices/
│   ├── sensor.py              # Member 2 – Sensor management
│   ├── device.py              # Member 4 – Device ID/IP
│   └── data_generator.py      # Member 3 – Sensor readings
│
├── networking/
│   ├── packet.py              # Member 5 – Packet structure
│   ├── gateway.py             # Member 6 – Gateway
│   ├── server.py              # Member 7 – Server
│   ├── transmission.py        # Member 8 – Delay/transmission
│   └── packet_loss.py         # Member 9 – Loss/errors
│
├── gui/
│   ├── dashboard.py           # Member 10 – Main GUI
│   ├── topology.py            # Network topology
│   └── animation.py           # Packet animation
│
├── testing/
│   ├── test_sensors.py        # Member 11
│   ├── test_packets.py
│   └── test_network.py
│
├── results/
│   ├── graphs.py              # Member 11
│   └── data/
│
└── README.md                  # Documentation
```

## How the Code Connects

```text
                    main.py
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Sensor Manager      Configuration
              │
              ▼
       Data Generator
              │
              ▼
       Device Manager
              │
              ▼
       Packet Manager
              │
              ▼
     Network Simulation
        ┌─────┴─────┐
        ▼           ▼
     Delay       Packet Loss
        │           │
        └─────┬─────┘
              ▼
           Gateway
              │
              ▼
           Server
              │
        ┌─────┴─────┐
        ▼           ▼
       GUI        Results
                  / Tests
```

## Main Data Flow

The core data flow is:

```text
Sensor
  ↓
SensorReading
  ↓
Packet
  ↓
Network
  ↓
Gateway
  ↓
Server
```

## Module Interfaces

Members should avoid depending directly on the internal implementation of another member's module. Use clear classes and interfaces between modules.

### Example

```python
reading = sensor.generate_reading()

packet = Packet(
    source=sensor.device_id,
    destination=gateway.device_id,
    data=reading
)

network.transmit(packet)

gateway.receive(packet)

server.receive(packet)
```

## Member Responsibilities

| Member | Module | Main Responsibility |
|---|---|---|
| 1 | System Architecture & Integration | Overall project structure, integration, and `main.py` |
| 2 | Virtual Sensor Management | Sensor creation, removal, configuration |
| 3 | Sensor Data Generation | Generate realistic sensor readings |
| 4 | Device ID & IP Management | Device IDs, IP addresses, and status |
| 5 | Packet Creation & Management | Packet structure and packet metadata |
| 6 | Gateway Simulation | Receive and forward packets |
| 7 | Server Simulation | Receive, process, and store packets |
| 8 | Delay & Transmission Simulation | Transmission and network delay |
| 9 | Packet Loss & Error Simulation | Packet drops and transmission errors |
| 10 | GUI & Visualization | Dashboard, topology, and packet animation |
| 11 | Testing, Graphs & Documentation | Tests, graphs, results, and documentation |

## Integration Principle

Member 1 maintains the central integration layer, but each member develops their assigned module independently.

The final system should follow:

```text
Sensor → Data → Packet → Network Conditions → Gateway → Server → GUI
```

All modules should communicate through defined interfaces so that individual implementations can be replaced or updated without breaking the entire system.
