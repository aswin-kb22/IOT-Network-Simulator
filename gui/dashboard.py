import tkinter as tk
import time
from tkinter import ttk, messagebox

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

        # Optional live performance graphs
        self.performance_window = None
        self.performance_canvases = {}
        self.performance_history = {
            "delivery": [],
            "delay": [],
            "throughput": []
        }
        self._last_graph_sample_time = None

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
        self.root.protocol("WM_DELETE_WINDOW", self._close_window)

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
        self.refresh_sensor_selector()

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

        # Dynamic sensor management
        ttk.Separator(self.controls_frame, orient="horizontal").grid(
            row=1, column=0, columnspan=7, sticky="ew", pady=8
        )

        ttk.Button(
            self.controls_frame,
            text="Add Sensor",
            command=self.add_sensor_dialog
        ).grid(row=2, column=0, padx=5, pady=3, sticky="w")

        ttk.Label(self.controls_frame, text="Sensor:").grid(
            row=2, column=1, padx=(10, 3), sticky="e"
        )

        self.sensor_selector = ttk.Combobox(
            self.controls_frame,
            state="readonly",
            width=14
        )
        self.sensor_selector.grid(row=2, column=2, padx=5, pady=3)

        ttk.Button(
            self.controls_frame,
            text="Remove Sensor",
            command=self.remove_selected_sensor
        ).grid(row=2, column=3, padx=5, pady=3)

        self.toggle_sensor_button = ttk.Button(
            self.controls_frame,
            text="Activate / Deactivate",
            command=self.toggle_selected_sensor
        )
        self.toggle_sensor_button.grid(row=2, column=4, columnspan=2, padx=5, pady=3)

        ttk.Button(
            self.controls_frame,
            text="Performance Graphs",
            command=self.open_performance_graphs
        ).grid(row=2, column=6, padx=8, pady=3)

        ttk.Button(
            self.controls_frame, text="Network Conditions",
            command=self.open_network_conditions
        ).grid(row=2, column=7, padx=8, pady=3)

        self.refresh_sensor_selector()

    def open_network_conditions(self):
        """Open controls that change the live network model."""
        window = tk.Toplevel(self.root)
        window.title("Network Conditions")
        window.transient(self.root)
        window.resizable(False, False)
        frame = ttk.Frame(window, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        loss_var = tk.DoubleVar(value=self.simulation.packet_loss.get_loss_probability() * 100)
        base_var = tk.DoubleVar(value=self.simulation.transmission.base_delay * 1000)
        variation_var = tk.DoubleVar(value=self.simulation.transmission.delay_variation * 1000)
        queue_var = tk.IntVar(value=self.simulation.gateway.get_queue_limit())
        value_labels = {}

        def add_slider(row, title, variable, low, high, suffix):
            ttk.Label(frame, text=title).grid(row=row, column=0, sticky="w", pady=6)
            slider = ttk.Scale(frame, from_=low, to=high, variable=variable, orient="horizontal", length=260)
            slider.grid(row=row, column=1, padx=10, pady=6)
            label = ttk.Label(frame, width=12)
            label.grid(row=row, column=2, sticky="e")
            value_labels[title] = (label, variable, suffix)
            def update_label(_value=None):
                label.config(text=f"{variable.get():.0f}{suffix}" if suffix in ("%", " ms") else f"{variable.get():.2f}{suffix}")
            slider.configure(command=update_label)
            update_label()

        add_slider(0, "Packet loss", loss_var, 0, 100, "%")
        add_slider(1, "Base delay", base_var, 0, 500, " ms")
        add_slider(2, "Delay variation", variation_var, 0, 250, " ms")
        ttk.Label(frame, text="Gateway queue limit").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Spinbox(frame, from_=1, to=500, textvariable=queue_var, width=10).grid(row=3, column=1, sticky="w", padx=10)

        def apply():
            try:
                self.simulation.apply_network_conditions(loss_var.get(), base_var.get(), variation_var.get(), queue_var.get())
                messagebox.showinfo("Network Conditions", "Settings applied to the running simulator.", parent=window)
            except (ValueError, TypeError) as error:
                messagebox.showerror("Invalid settings", str(error), parent=window)

        buttons = ttk.Frame(frame)
        buttons.grid(row=4, column=0, columnspan=3, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text="Apply", command=apply).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="Close", command=window.destroy).grid(row=0, column=1, padx=5)

    # ---------------------------------------------------------
    # DYNAMIC SENSOR MANAGEMENT
    # ---------------------------------------------------------

    def refresh_sensor_selector(self):
        """Refresh the sensor dropdown after sensor changes."""
        if not hasattr(self, "sensor_selector") or self.sensor_selector is None:
            return

        try:
            sensors = self.simulation.sensor_manager.get_all_sensors()
            ids = [sensor.device_id for sensor in sensors]
            self.sensor_selector["values"] = ids
            current = self.sensor_selector.get()
            if current not in ids:
                self.sensor_selector.set(ids[0] if ids else "")
        except Exception as error:
            print("Could not refresh sensor list:", error)

    def add_sensor_dialog(self):
        """Open a small form and ask the simulator to create a sensor."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add IoT Sensor")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Sensor type:").grid(
            row=0, column=0, padx=6, pady=7, sticky="w"
        )
        type_var = tk.StringVar(value="temperature")
        type_box = ttk.Combobox(
            frame,
            textvariable=type_var,
            values=("temperature", "humidity", "light", "motion", "soil_moisture"),
            state="readonly",
            width=20
        )
        type_box.grid(row=0, column=1, padx=6, pady=7)

        ttk.Label(frame, text="Sampling interval (seconds):").grid(
            row=1, column=0, padx=6, pady=7, sticky="w"
        )
        interval_var = tk.StringVar(value="2")
        interval_entry = ttk.Entry(frame, textvariable=interval_var, width=23)
        interval_entry.grid(row=1, column=1, padx=6, pady=7)

        def submit():
            try:
                interval = float(interval_var.get().strip())
                if interval <= 0:
                    raise ValueError("Sampling interval must be greater than 0.")
                sensor_type = type_var.get().strip().lower()
                sensor = self.simulation.add_sensor(sensor_type, interval)

                self.refresh_sensor_selector()
                self.update_activity({
                    "event": f"Added {sensor.device_id} ({sensor_type}, interval={interval:g}s)"
                })
                dialog.destroy()
            except Exception as error:
                messagebox.showerror(
                    "Unable to add sensor", str(error), parent=dialog
                )

        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="e")
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(buttons, text="Add", command=submit).grid(
            row=0, column=1, padx=5
        )
        interval_entry.focus_set()

    def remove_selected_sensor(self):
        device_id = self.sensor_selector.get() if hasattr(self, "sensor_selector") else ""
        if not device_id:
            messagebox.showinfo("Remove Sensor", "There are no sensors to remove.", parent=self.root)
            return

        if not messagebox.askyesno(
            "Remove Sensor", f"Remove sensor {device_id}?", parent=self.root
        ):
            return

        try:
            removed = self.simulation.remove_sensor(device_id)
            if not removed:
                messagebox.showerror("Remove Sensor", f"Sensor {device_id} was not found.", parent=self.root)
                self.refresh_sensor_selector()
                return

            self.refresh_sensor_selector()
            self.update_activity({"event": f"Removed sensor {device_id}"})
        except Exception as error:
            messagebox.showerror("Remove Sensor", str(error), parent=self.root)

    def toggle_selected_sensor(self):
        device_id = self.sensor_selector.get() if hasattr(self, "sensor_selector") else ""
        if not device_id:
            messagebox.showinfo("Sensor Status", "Select a sensor first.", parent=self.root)
            return

        sensor = self.simulation.sensor_manager.get_sensor(device_id)
        if sensor is None:
            self.refresh_sensor_selector()
            messagebox.showerror("Sensor Status", "The selected sensor no longer exists.", parent=self.root)
            return

        if sensor.get_status() == "ACTIVE":
            sensor.deactivate()
            status = "INACTIVE"
        else:
            sensor.activate()
            status = "ACTIVE"

        if self.topology is not None:
            try:
                self.topology.update_node_status(device_id, status)
            except Exception as error:
                print("Could not update sensor node status:", error)

        self.update_activity({"event": f"{device_id} is now {status}"})
        self.refresh_sensor_selector()

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

        # Clear performance graph history
        for values in self.performance_history.values():
            values.clear()
        self._last_graph_sample_time = None
        if self.performance_window is not None:
            self._draw_performance_graphs()

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

            if self.animation is not None:

                self.animation.set_animation_speed(
                    speed
                )

            self.speed_value_label.config(
                text=f"{speed:.1f}x"
            )

        except (
            ValueError,
            TypeError,
            AttributeError
        ):

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
    # PERFORMANCE GRAPHS
    # ---------------------------------------------------------

    def open_performance_graphs(self):
        """Open a separate window containing live performance charts."""
        if self.performance_window is not None:
            try:
                if self.performance_window.winfo_exists():
                    self.performance_window.deiconify()
                    self.performance_window.lift()
                    self._draw_performance_graphs()
                    return
            except tk.TclError:
                pass

        self.performance_window = tk.Toplevel(self.root)
        self.performance_window.title("IoT Network Simulator - Performance Analysis")
        self.performance_window.geometry("850x760")
        self.performance_window.minsize(650, 600)
        self.performance_window.protocol(
            "WM_DELETE_WINDOW",
            self._close_performance_graphs
        )

        for row in range(3):
            self.performance_window.rowconfigure(row, weight=1)
        self.performance_window.columnconfigure(0, weight=1)

        chart_specs = [
            ("delivery", "Packet Delivery vs Packet Loss", "Packets"),
            ("delay", "Average Network Delay", "Seconds"),
            ("throughput", "Throughput", "Packets / simulation-time unit")
        ]

        for row, (key, title, ylabel) in enumerate(chart_specs):
            frame = ttk.LabelFrame(
                self.performance_window,
                text=title,
                padding=6
            )
            frame.grid(row=row, column=0, padx=10, pady=6, sticky="nsew")
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

            canvas = tk.Canvas(
                frame,
                height=180,
                background="white",
                highlightthickness=1,
                highlightbackground="#cccccc"
            )
            canvas.grid(row=0, column=0, sticky="nsew")
            self.performance_canvases[key] = canvas

        self._draw_performance_graphs()

    def _close_performance_graphs(self):
        if self.performance_window is not None:
            try:
                self.performance_window.destroy()
            except tk.TclError:
                pass
        self.performance_window = None
        self.performance_canvases = {}

    def _sample_performance_metrics(self, summary, simulation_time):
        """Sample at most twice per second while the graph window is open."""
        if self.performance_window is None:
            return
        try:
            if not self.performance_window.winfo_exists():
                return
        except tk.TclError:
            return

        now = time.monotonic()
        if self._last_graph_sample_time is not None and now - self._last_graph_sample_time < 0.5:
            return
        self._last_graph_sample_time = now

        delivered = int(summary.get("packets_delivered", 0) or 0)
        lost = int(summary.get("packets_lost", 0) or 0)
        delay = float(summary.get("average_delay", 0) or 0)
        throughput = float(summary.get("throughput", 0) or 0)

        self.performance_history["delivery"].append((delivered, lost))
        self.performance_history["delay"].append(delay)
        self.performance_history["throughput"].append(throughput)

        # Keep the chart responsive during long runs.
        for values in self.performance_history.values():
            if len(values) > 120:
                del values[:-120]

        self._draw_performance_graphs()

    def _draw_performance_graphs(self):
        """Draw simple charts with Tkinter Canvas; no external plotting package required."""
        if not self.performance_canvases:
            return

        self._draw_line_chart(
            self.performance_canvases.get("delivery"),
            "Delivered", "Lost",
            self.performance_history["delivery"],
            paired=True
        )
        self._draw_line_chart(
            self.performance_canvases.get("delay"),
            "Average delay (s)", None,
            self.performance_history["delay"]
        )
        self._draw_line_chart(
            self.performance_canvases.get("throughput"),
            "Throughput", None,
            self.performance_history["throughput"]
        )

    def _draw_line_chart(self, canvas, series_name, second_name, values, paired=False):
        if canvas is None:
            return
        try:
            width = max(canvas.winfo_width(), 300)
            height = max(canvas.winfo_height(), 130)
            canvas.delete("chart")
            left, right, top, bottom = 48, width - 18, 22, height - 30
            canvas.create_line(left, top, left, bottom, fill="#555555", tags="chart")
            canvas.create_line(left, bottom, right, bottom, fill="#555555", tags="chart")
            canvas.create_text(8, 10, anchor="nw", text=series_name, fill="#2463a6", tags="chart")
            if second_name:
                canvas.create_text(125, 10, anchor="nw", text=second_name, fill="#c43d3d", tags="chart")

            if not values:
                canvas.create_text(
                    (left + right) / 2,
                    (top + bottom) / 2,
                    text="Start the simulation to collect data",
                    fill="#777777",
                    tags="chart"
                )
                return

            if paired:
                series = [
                    ([point[0] for point in values], "#2463a6"),
                    ([point[1] for point in values], "#c43d3d")
                ]
            else:
                series = [(values, "#2463a6")]

            all_numbers = [float(v) for seq, _ in series for v in seq]
            max_value = max(all_numbers + [1.0])
            min_value = min(all_numbers + [0.0])
            if max_value == min_value:
                max_value = min_value + 1.0

            # Horizontal guide lines and scale labels
            for fraction in (0, 0.5, 1):
                y = bottom - fraction * (bottom - top)
                label = min_value + fraction * (max_value - min_value)
                canvas.create_line(left, y, right, y, fill="#e5e7eb", tags="chart")
                canvas.create_text(left - 6, y, anchor="e", text=f"{label:.2g}", fill="#555555", tags="chart")

            plot_width = right - left
            plot_height = bottom - top
            for sequence, line_color in series:
                points = []
                count = len(sequence)
                for index, value in enumerate(sequence):
                    x = left if count == 1 else left + index * plot_width / (count - 1)
                    y = bottom - (float(value) - min_value) / (max_value - min_value) * plot_height
                    points.extend((x, y))
                if len(points) >= 4:
                    canvas.create_line(*points, fill=line_color, width=2, tags="chart")
                elif len(points) == 2:
                    x, y = points
                    canvas.create_oval(x-3, y-3, x+3, y+3, fill=line_color, outline=line_color, tags="chart")

            canvas.create_text(left, height - 8, anchor="sw", text="Older samples", fill="#555555", tags="chart")
            canvas.create_text(right, height - 8, anchor="se", text="Latest", fill="#555555", tags="chart")
        except tk.TclError:
            pass

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

            self._sample_performance_metrics(summary, simulation_time)

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

    # =========================================================
# PACKET ANIMATION
# =========================================================

    def animate_packet(
        self,
        packet,
        source,
        destination,
        duration=None
    ):

        if self.animation is None:
            return

        try:

            # Convert device IDs into topology positions
            source_position = self.topology.get_node_position(
                source
            )

            destination_position = self.topology.get_node_position(
                destination
            )

            if source_position is None:
                return

            if destination_position is None:
                return

            self.animation.animate_packet(
                packet,
                source_position,
                destination_position,
                duration
            )

        except Exception as error:

            print(
                "Animation error:",
                error
            )

    def update_packet_status(
    self,
    packet_id,
    status
    ):

        if self.animation is None:
            return

        try:

            self.animation.show_packet_status(
            packet_id,
            status
        )

        except Exception as error:

            print(
                "Packet status animation error:",
                error
            )

    
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