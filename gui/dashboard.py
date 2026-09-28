import tkinter as tk
from tkinter import ttk

from gui.topology import Topology
from gui.animation import PacketAnimation


class Dashboard:

    def __init__(self, simulation):
        self.simulation = simulation

        # Root window
        self.root = None

        # Tkinter variables
        self.simulation_speed = None

        self.status_text = None
        self.time_text = None

        self.generated_text = None
        self.forwarded_text = None
        self.delivered_text = None
        self.lost_text = None

        self.loss_rate_text = None
        self.delivery_rate_text = None
        self.delay_text = None
        self.throughput_text = None

        # Frames
        self.statistics_frame = None
        self.activity_frame = None
        self.topology_frame = None
        self.controls_frame = None

        # Widgets
        self.activity_list = None

        self.start_button = None
        self.pause_button = None
        self.reset_button = None

        self.speed_scale = None
        self.speed_value_label = None

        # Topology
        self.canvas = None
        self.topology = None
        self.animation = None
        self.topology_initialized = False

        # Refresh
        self.refresh_job = None

    # ---------------------------------------------------------
    # WINDOW
    # ---------------------------------------------------------

    def create_window(self):

        self.root = tk.Tk()

        self.root.title("IoT Network Simulator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # -----------------------------------------------------
        # Tkinter variables MUST be created after Tk()
        # -----------------------------------------------------

        self.simulation_speed = tk.DoubleVar(
            master=self.root,
            value=1.0
        )

        self.status_text = tk.StringVar(
            master=self.root,
            value="Simulation: Stopped"
        )

        self.time_text = tk.StringVar(
            master=self.root,
            value="Simulation Time: 0"
        )

        self.generated_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        self.forwarded_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        self.delivered_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        self.lost_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        self.loss_rate_text = tk.StringVar(
            master=self.root,
            value="0%"
        )

        self.delivery_rate_text = tk.StringVar(
            master=self.root,
            value="0%"
        )

        self.delay_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        self.throughput_text = tk.StringVar(
            master=self.root,
            value="0"
        )

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        # Topology
        self.create_topology_panel()

        # Right-side statistics
        self.create_statistics_panel()

        # Bottom controls
        self.create_controls()

        # Activity panel
        self.create_activity_panel()

        # Close handler
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self._close_window
        )

    # ---------------------------------------------------------
    # TOPOLOGY
    # ---------------------------------------------------------

    def create_topology_panel(self):

        self.topology_frame = ttk.LabelFrame(
            self.root,
            text="Network Topology",
            padding=10
        )

        self.topology_frame.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.topology_frame.rowconfigure(0, weight=1)
        self.topology_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.topology_frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Topology object
        self.topology = Topology(self.canvas)

        # Packet animation object
        self.animation = PacketAnimation(self.canvas)

        self.build_topology()

    # ---------------------------------------------------------

    def build_topology(self):

        if self.topology is None:
            return

        try:
            self.topology.clear_topology()
        except Exception:
            pass

        # -----------------------------------------------------
        # Add sensors
        # -----------------------------------------------------

        sensors = self.simulation.sensor_manager.get_all_sensors()

        for sensor in sensors:

            try:
                self.topology.add_sensor_node(sensor)
            except TypeError:

                # Fallback for topology implementations
                self.topology.add_sensor_node(
                    sensor.device_id,
                    sensor.sensor_type
                )

        # -----------------------------------------------------
        # Add gateway
        # -----------------------------------------------------

        gateway = self.simulation.gateway

        try:
            self.topology.add_gateway_node(gateway)
        except TypeError:
            self.topology.add_gateway_node(
                gateway.device_id
            )

        # -----------------------------------------------------
        # Add server
        # -----------------------------------------------------

        server = self.simulation.server

        try:
            self.topology.add_server_node(server)
        except TypeError:
            self.topology.add_server_node(
                server.device_id
            )

        # -----------------------------------------------------
        # Connect sensors -> gateway
        # -----------------------------------------------------

        for sensor in sensors:

            try:
                self.topology.connect_nodes(
                    sensor.device_id,
                    gateway.device_id
                )
            except Exception:
                pass

        # -----------------------------------------------------
        # Gateway -> server
        # -----------------------------------------------------

        try:
            self.topology.connect_nodes(
                gateway.device_id,
                server.device_id
            )
        except Exception:
            pass

        self.topology_initialized = True

    # ---------------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------------

    def create_statistics_panel(self):

        self.statistics_frame = ttk.LabelFrame(
            self.root,
            text="Simulation Statistics",
            padding=10
        )

        self.statistics_frame.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(10, 5),
            sticky="nsew"
        )

        self.statistics_frame.columnconfigure(
            1,
            weight=1
        )

        # Status
        self._add_stat_row(
            0,
            "Status",
            self.status_text
        )

        self._add_stat_row(
            1,
            "Simulation Time",
            self.time_text
        )

        self._add_stat_row(
            2,
            "Packets Generated",
            self.generated_text
        )

        self._add_stat_row(
            3,
            "Packets Forwarded",
            self.forwarded_text
        )

        self._add_stat_row(
            4,
            "Packets Delivered",
            self.delivered_text
        )

        self._add_stat_row(
            5,
            "Packets Lost",
            self.lost_text
        )

        self._add_stat_row(
            6,
            "Packet Loss",
            self.loss_rate_text
        )

        self._add_stat_row(
            7,
            "Delivery Rate",
            self.delivery_rate_text
        )

        self._add_stat_row(
            8,
            "Average Delay",
            self.delay_text
        )

        self._add_stat_row(
            9,
            "Throughput",
            self.throughput_text
        )

    # ---------------------------------------------------------

    def _add_stat_row(self, row, label, variable):

        ttk.Label(
            self.statistics_frame,
            text=label + ":",
            font=("Arial", 10)
        ).grid(
            row=row,
            column=0,
            padx=5,
            pady=4,
            sticky="w"
        )

        ttk.Label(
            self.statistics_frame,
            textvariable=variable,
            font=("Arial", 10, "bold")
        ).grid(
            row=row,
            column=1,
            padx=5,
            pady=4,
            sticky="e"
        )

    # ---------------------------------------------------------
    # ACTIVITY
    # ---------------------------------------------------------

    def create_activity_panel(self):

        self.activity_frame = ttk.LabelFrame(
            self.root,
            text="Recent Activity",
            padding=10
        )

        self.activity_frame.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(5, 10),
            sticky="nsew"
        )

        self.activity_frame.rowconfigure(
            0,
            weight=1
        )

        self.activity_frame.columnconfigure(
            0,
            weight=1
        )

        # Listbox
        self.activity_list = tk.Listbox(
            self.activity_frame,
            height=8,
            font=("Consolas", 9)
        )

        self.activity_list.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.activity_frame,
            orient="vertical",
            command=self.activity_list.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.activity_list.configure(
            yscrollcommand=scrollbar.set
        )

    # ---------------------------------------------------------
    # CONTROLS
    # ---------------------------------------------------------

    def create_controls(self):

        self.controls_frame = ttk.LabelFrame(
            self.root,
            text="Simulation Controls",
            padding=10
        )

        self.controls_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=(0, 10),
            sticky="ew"
        )

        # Buttons
        self.start_button = ttk.Button(
            self.controls_frame,
            text="Start",
            command=self.start_simulation
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.pause_button = ttk.Button(
            self.controls_frame,
            text="Pause",
            command=self.pause_simulation
        )

        self.pause_button.grid(
            row=0,
            column=1,
            padx=5
        )

        self.reset_button = ttk.Button(
            self.controls_frame,
            text="Reset",
            command=self.reset_simulation
        )

        self.reset_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # Speed label
        ttk.Label(
            self.controls_frame,
            text="Simulation Speed:"
        ).grid(
            row=0,
            column=3,
            padx=(30, 5)
        )

        # Speed slider
        self.speed_scale = ttk.Scale(
            self.controls_frame,
            from_=0.1,
            to=5.0,
            orient="horizontal",
            variable=self.simulation_speed,
            command=self.set_simulation_speed,
            length=200
        )

        self.speed_scale.grid(
            row=0,
            column=4,
            padx=5
        )

        # Speed value
        self.speed_value_label = ttk.Label(
            self.controls_frame,
            text="1.0x"
        )

        self.speed_value_label.grid(
            row=0,
            column=5,
            padx=5
        )

    # ---------------------------------------------------------
    # START
    # ---------------------------------------------------------

    def start_simulation(self):

        if self.simulation.running:
            return

        self.status_text.set(
            "Simulation: Running"
        )

        try:
            self.simulation.start_simulation()
        except Exception as error:
            print(
                "Error starting simulation:",
                error
            )

        self.refresh()

    # ---------------------------------------------------------
    # PAUSE
    # ---------------------------------------------------------

    def pause_simulation(self):

        try:
            self.simulation.pause_simulation()
        except Exception as error:
            print(
                "Error pausing simulation:",
                error
            )

        self.status_text.set(
            "Simulation: Paused"
        )

    # ---------------------------------------------------------
    # RESET
    # ---------------------------------------------------------

    def reset_simulation(self):

        try:
            self.simulation.reset_simulation()
        except Exception as error:
            print(
                "Error resetting simulation:",
                error
            )

        # Clear activity
        if self.activity_list is not None:
            self.activity_list.delete(
                0,
                tk.END
            )

        # Clear animations
        if self.animation is not None:

            try:
                self.animation.clear_animations()
            except Exception:
                pass

        # Rebuild topology
        self.build_topology()

        # Reset displayed values
        self.status_text.set(
            "Simulation: Stopped"
        )

        self.time_text.set(
            "Simulation Time: 0"
        )

        self.generated_text.set("0")
        self.forwarded_text.set("0")
        self.delivered_text.set("0")
        self.lost_text.set("0")
        self.loss_rate_text.set("0%")
        self.delivery_rate_text.set("0%")
        self.delay_text.set("0")
        self.throughput_text.set("0")

    # ---------------------------------------------------------
    # SPEED
    # ---------------------------------------------------------

    def set_simulation_speed(self, value):

        try:
            speed = float(value)

            if speed <= 0:
                speed = 0.1

            self.simulation.set_simulation_speed(
                speed
            )

            self.speed_value_label.config(
                text=f"{speed:.1f}x"
            )

        except (ValueError, TypeError, AttributeError):
            pass

    # ---------------------------------------------------------
    # UPDATE STATISTICS
    # ---------------------------------------------------------

    def update_statistics(self, summary):

        if not summary:
            return

        # Generated
        self.generated_text.set(
            str(
                summary.get(
                    "packets_generated",
                    0
                )
            )
        )

        # Forwarded
        self.forwarded_text.set(
            str(
                summary.get(
                    "packets_forwarded",
                    0
                )
            )
        )

        # Delivered
        self.delivered_text.set(
            str(
                summary.get(
                    "packets_delivered",
                    0
                )
            )
        )

        # Lost
        self.lost_text.set(
            str(
                summary.get(
                    "packets_lost",
                    0
                )
            )
        )

        # Packet loss
        loss = summary.get(
            "packet_loss_percentage",
            summary.get(
                "packet_loss_rate",
                summary.get(
                    "packet_loss",
                    0
                )
            )
        )

        try:
            self.loss_rate_text.set(
                f"{float(loss):.2f}%"
            )
        except (ValueError, TypeError):
            self.loss_rate_text.set(
                str(loss)
            )

        # Delivery rate
        delivery = summary.get(
            "delivery_rate",
            0
        )

        try:
            self.delivery_rate_text.set(
                f"{float(delivery):.2f}%"
            )
        except (ValueError, TypeError):
            self.delivery_rate_text.set(
                str(delivery)
            )

        # Delay
        delay = summary.get(
            "average_delay",
            0
        )

        try:
            self.delay_text.set(
                f"{float(delay):.4f} s"
            )
        except (ValueError, TypeError):
            self.delay_text.set(
                str(delay)
            )

        # Throughput
        throughput = summary.get(
            "throughput",
            0
        )

        try:
            self.throughput_text.set(
                f"{float(throughput):.2f} packets/s"
            )
        except (ValueError, TypeError):
            self.throughput_text.set(
                str(throughput)
            )

    # ---------------------------------------------------------
    # ACTIVITY UPDATE
    # ---------------------------------------------------------

    def update_activity(self, event):

        if self.activity_list is None:
            return

        if isinstance(event, dict):

            event_text = event.get(
                "event",
                str(event)
            )

        else:
            event_text = str(event)

        self.activity_list.insert(
            tk.END,
            event_text
        )

        # Keep only recent events
        max_events = 50

        while self.activity_list.size() > max_events:

            self.activity_list.delete(
                0
            )

        # Scroll to bottom
        self.activity_list.yview_moveto(
            1.0
        )

    # ---------------------------------------------------------
    # UPDATE NODE STATUS
    # ---------------------------------------------------------

    def update_node_statuses(self):

        if self.topology is None:
            return

        # Sensors
        try:

            sensors = (
                self.simulation
                .sensor_manager
                .get_all_sensors()
            )

            for sensor in sensors:

                try:
                    self.topology.update_node_status(
                        sensor.device_id,
                        sensor.get_status()
                    )
                except Exception:
                    pass

        except Exception:
            pass

        # Gateway
        try:
            self.topology.update_node_status(
                self.simulation.gateway.device_id,
                self.simulation.gateway.status
            )
        except Exception:
            pass

        # Server
        try:
            self.topology.update_node_status(
                self.simulation.server.device_id,
                self.simulation.server.status
            )
        except Exception:
            pass

    # ---------------------------------------------------------
    # REFRESH
    # ---------------------------------------------------------

    def refresh(self):

        if self.root is None:
            return

        try:

            # Simulation time
            simulation_time = (
                self.simulation
                .get_simulation_time()
            )

            self.time_text.set(
                f"Simulation Time: {simulation_time}"
            )

            # Metrics
            summary = (
                self.simulation
                .metrics
                .get_summary()
            )

            try:

                summary["throughput"] = (
                    self.simulation
                    .metrics
                    .calculate_throughput(
                        simulation_time
                    )
                )

            except Exception:
                summary["throughput"] = 0

            summary["packet_loss_rate"] = (
                summary.get(
                    "packet_loss_percentage",
                    0
                )
            )

            self.update_statistics(
                summary
            )

            # Node statuses
            self.update_node_statuses()

            # Activity events
            try:

                events = (
                    self.simulation
                    .metrics
                    .events
                )

                if events:

                    last_event = events[-1]

                    # Avoid continuously duplicating
                    # the same event
                    event_text = last_event.get(
                        "event",
                        ""
                    )

                    if (
                        not self.activity_list.size()
                        or self.activity_list.get(
                            tk.END
                        ) != event_text
                    ):
                        self.update_activity(
                            last_event
                        )

            except Exception:
                pass

            # Continue simulation
            if self.simulation.running:

                self.simulation.update_simulation()

            # Schedule next refresh
            if self.root is not None:

                self.refresh_job = (
                    self.root.after(
                        100,
                        self.refresh
                    )
                )

        except tk.TclError:
            # Window already closed
            return

        except Exception as error:

            print(
                "Dashboard refresh error:",
                error
            )

            if self.root is not None:

                try:
                    self.refresh_job = (
                        self.root.after(
                            100,
                            self.refresh
                        )
                    )
                except Exception:
                    pass

    # ---------------------------------------------------------
    # RUN
    # ---------------------------------------------------------

    def run(self):

        self.create_window()

        self.refresh()

        self.root.mainloop()

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def _close_window(self):

        try:
            self.simulation.pause_simulation()
        except Exception:
            pass

        if self.refresh_job is not None:

            try:
                self.root.after_cancel(
                    self.refresh_job
                )
            except Exception:
                pass

        try:
            self.root.destroy()
        except Exception:
            pass

        self.root = None

    # ---------------------------------------------------------
    # FORMATTING HELPERS
    # ---------------------------------------------------------

    @staticmethod
    def format_number(value, decimals=2):

        try:
            return f"{float(value):.{decimals}f}"
        except (ValueError, TypeError):
            return str(value)

    @staticmethod
    def format_percentage(value):

        try:
            return f"{float(value):.2f}%"
        except (ValueError, TypeError):
            return str(value)