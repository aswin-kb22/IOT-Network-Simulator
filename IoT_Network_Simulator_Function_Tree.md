# IoT Network Simulator — Overall Function Tree

## Project Structure

```text
IOT-Network-Simulator/
│
├── main.py
│   └── main()
│
├── config/
│   └── config.py
│       └── Global configuration values
│
├── devices/
│   │
│   ├── device.py
│   │   ├── Device
│   │   │   ├── __init__(device_id, ip_address, device_type)
│   │   │   ├── activate()
│   │   │   ├── deactivate()
│   │   │   ├── set_ip(ip_address)
│   │   │   ├── get_ip()
│   │   │   ├── get_device_id()
│   │   │   ├── get_status()
│   │   │   └── get_info()
│   │   │
│   │   └── DeviceManager
│   │       ├── __init__()
│   │       ├── add_device(device)
│   │       ├── remove_device(device_id)
│   │       ├── get_device(device_id)
│   │       └── get_all_devices()
│   │
│   ├── sensor.py
│   │   ├── Sensor
│   │   │   ├── __init__(device_id, sensor_type, interval)
│   │   │   ├── activate()
│   │   │   ├── deactivate()
│   │   │   ├── set_interval(interval)
│   │   │   ├── set_sensor_type(sensor_type)
│   │   │   ├── get_status()
│   │   │   └── get_info()
│   │   │
│   │   └── SensorManager
│   │       ├── __init__()
│   │       ├── add_sensor(sensor)
│   │       ├── remove_sensor(device_id)
│   │       ├── get_sensor(device_id)
│   │       └── get_all_sensors()
│   │
│   └── data_generator.py
│       └── DataGenerator
│           ├── __init__()
│           ├── generate_temperature()
│           ├── generate_humidity()
│           ├── generate_light()
│           ├── generate_motion()
│           ├── generate_soil_moisture()
│           └── generate_reading(sensor_type)
│
├── networking/
│   │
│   ├── packet.py
│   │   └── Packet
│   │       ├── __init__(packet_id, source, destination, data)
│   │       ├── update_status(status)
│   │       ├── add_timestamp(event, timestamp)
│   │       ├── get_status()
│   │       └── get_info()
│   │
│   ├── transmission.py
│   │   └── Transmission
│   │       ├── __init__(base_delay, delay_variation)
│   │       ├── calculate_delay()
│   │       ├── transmit(packet, source, destination)
│   │       └── get_transmission_time()
│   │
│   ├── packet_loss.py
│   │   └── PacketLoss
│   │       ├── __init__(loss_probability)
│   │       ├── is_packet_lost()
│   │       ├── apply_loss(packet)
│   │       └── get_loss_probability()
│   │
│   ├── gateway.py
│   │   └── Gateway
│   │       ├── __init__(device_id, ip_address)
│   │       ├── receive(packet)
│   │       ├── validate_packet(packet)
│   │       ├── queue_packet(packet)
│   │       ├── process_queue()
│   │       ├── forward_packet(packet)
│   │       └── get_queue_size()
│   │
│   └── server.py
│       └── Server
│           ├── __init__(device_id, ip_address)
│           ├── receive(packet)
│           ├── process_packet(packet)
│           ├── store_packet(packet)
│           ├── get_received_packets()
│           └── get_packet_count()
│
├── results/
│   │
│   ├── metrics.py
│   │   └── Metrics
│   │       ├── __init__()
│   │       ├── record_packet_generated(packet)
│   │       ├── record_packet_forwarded(packet)
│   │       ├── record_packet_delivered(packet)
│   │       ├── record_packet_lost(packet)
│   │       ├── calculate_packet_loss()
│   │       ├── calculate_average_delay()
│   │       ├── calculate_delivery_rate()
│   │       ├── calculate_throughput(simulation_time)
│   │       ├── calculate_queue_pressure(queue_size)
│   │       └── get_summary()
│   │
│   └── graphs.py
│       └── GraphGenerator
│           ├── __init__(metrics)
│           ├── plot_packet_statistics()
│           ├── plot_packet_loss()
│           ├── plot_delay()
│           ├── plot_delivery_rate()
│           ├── plot_throughput()
│           └── save_graph(figure, filename)
│
├── gui/
│   │
│   ├── dashboard.py
│   │   └── Dashboard
│   │       ├── __init__(simulation)
│   │       ├── create_window()
│   │       ├── create_controls()
│   │       ├── create_statistics_panel()
│   │       ├── create_activity_panel()
│   │       ├── update_statistics(metrics)
│   │       ├── update_activity(event)
│   │       ├── start_simulation()
│   │       ├── pause_simulation()
│   │       ├── reset_simulation()
│   │       ├── set_simulation_speed(speed)
│   │       └── run()
│   │
│   ├── topology.py
│   │   └── Topology
│   │       ├── __init__(canvas)
│   │       ├── add_sensor_node(sensor)
│   │       ├── add_gateway_node(gateway)
│   │       ├── add_server_node(server)
│   │       ├── connect_nodes(source, destination)
│   │       ├── remove_node(device_id)
│   │       ├── update_node_status(device_id, status)
│   │       └── clear_topology()
│   │
│   └── animation.py
│       └── PacketAnimation
│           ├── __init__(canvas)
│           ├── animate_packet(packet, source, destination)
│           ├── update_packet_position(packet_id, position)
│           ├── show_packet_status(packet_id, status)
│           ├── remove_packet(packet_id)
│           └── clear_animations()
│
└── testing/
    │
    ├── test_sensors.py
    │   ├── test_create_sensor()
    │   ├── test_sensor_activation()
    │   ├── test_sensor_deactivation()
    │   ├── test_sensor_configuration()
    │   ├── test_sensor_interval()
    │   ├── test_add_sensor()
    │   ├── test_remove_sensor()
    │   └── test_generate_reading()
    │
    ├── test_packets.py
    │   ├── test_create_packet()
    │   ├── test_packet_metadata()
    │   ├── test_packet_status()
    │   ├── test_packet_timestamp()
    │   ├── test_packet_status_update()
    │   └── test_packet_info()
    │
    └── test_network.py
        ├── test_transmission()
        ├── test_delay()
        ├── test_packet_loss()
        ├── test_gateway_receive()
        ├── test_gateway_queue()
        ├── test_gateway_forward()
        ├── test_server_receive()
        └── test_end_to_end_delivery()
```

## Core Execution Flow

```text
main()
 │
 ├── DeviceManager
 │
 ├── SensorManager
 │       │
 │       └── DataGenerator
 │               │
 │               ▼
 │            Reading
 │               │
 │               ▼
 │            Packet
 │               │
 │               ▼
 │          Transmission
 │          /           \
 │       Delay       PacketLoss
 │          \           /
 │               ▼
 │            Gateway
 │               │
 │               ▼
 │             Server
 │               │
 │               ▼
 │            Metrics
 │            /      \
 │           ▼        ▼
 │      Dashboard   Graphs
 │
 └── GUI
       ├── Topology
       └── Animation
```

## Module Boundaries

- `config.py` — global configuration values only
- `device.py` — device identity, IP address, and status
- `sensor.py` — virtual sensor creation and management
- `data_generator.py` — sensor value generation
- `packet.py` — packet structure and lifecycle
- `transmission.py` — transmission and delay simulation
- `packet_loss.py` — packet loss/error simulation
- `gateway.py` — packet reception, queuing, validation, and forwarding
- `server.py` — packet reception, processing, and storage
- `metrics.py` — network metric collection and calculation
- `graphs.py` — result visualization
- `dashboard.py` — main GUI controls and statistics
- `topology.py` — network topology visualization
- `animation.py` — packet-flow animation
- `testing/` — module and end-to-end tests
