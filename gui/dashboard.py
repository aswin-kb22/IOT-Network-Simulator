import tkinter as tk
from tkinter import ttk


class Dashboard:
    """
    Main GUI dashboard for the IoT Network Simulator.

    The Dashboard is responsible for:
        - Creating the main application window
        - Providing simulation controls
        - Displaying network statistics
        - Displaying recent simulation activity
        - Controlling simulation start/pause/reset
        - Controlling simulation speed
    """

    def __init__(self, simulation):
        """
        Initialize the dashboard.

        Parameters:
            simulation:
                Reference to the IoTNetworkSimulator object.
        """

        self.simulation = simulation

        self.root = None

        # GUI variables
        self.simulation_speed = tk.DoubleVar(value=1.0)

        self.status_text = tk.StringVar(
            value="Simulation: Stopped"
        )

        self.time_text = tk.StringVar(
            value="Simulation Time: 0"
        )

        # Statistics variables
        self.generated_text = tk.StringVar(value="0")
        self.forwarded_text = tk.StringVar(value="0")
        self.delivered_text = tk.StringVar(value="0")
        self.lost_text = tk.StringVar(value="0")
        self.loss_rate_text = tk.StringVar(value="0%")
        self.delivery_rate_text = tk.StringVar(value="0%")
        self.delay_text = tk.StringVar(value="0")
        self.throughput_text = tk.StringVar(value="0")

        # Widgets
        self.statistics_frame = None
        self.activity_frame = None
        self.activity_list = None

        self.start_button = None
        self.pause_button = None
        self.reset_button = None
        self.speed_scale = None

    # =========================================================
    # CREATE WINDOW
    # =========================================================

    def create_window(self):
        """
        Create and configure the main Tkinter window.
        """

        self.root = tk.Tk()

        self.root.title(
            "IoT Network Simulator"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.minsize(
            800,
            600
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self._close_window
        )

        # Main window grid
        self.root.columnconfigure(
            0,
            weight=1
        )

        self.root.columnconfigure(
            1,
            weight=2
        )

        self.root.rowconfigure(
            1,
            weight=1
        )

        # Title
        title_label = ttk.Label(
            self.root,
            text="IoT Network Simulator",
            font=("Arial", 20, "bold")
        )

        title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=15
        )

        # Create GUI sections
        self.create_controls()
        self.create_statistics_panel()
        self.create_activity_panel()

    # =========================================================
    # CREATE CONTROLS
    # =========================================================

    def create_controls(self):
        """
        Create simulation control buttons and speed control.
        """

        control_frame = ttk.LabelFrame(
            self.root,
            text="Simulation Controls",
            padding=10
        )

        control_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # Start button
        self.start_button = ttk.Button(
            control_frame,
            text="Start",
            command=self.start_simulation
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )

        # Pause button
        self.pause_button = ttk.Button(
            control_frame,
            text="Pause",
            command=self.pause_simulation
        )

        self.pause_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # Reset button
        self.reset_button = ttk.Button(
            control_frame,
            text="Reset",
            command=self.reset_simulation
        )

        self.reset_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # Status
        status_label = ttk.Label(
            control_frame,
            textvariable=self.status_text
        )

        status_label.grid(
            row=0,
            column=3,
            padx=20
        )

        # Simulation time
        time_label = ttk.Label(
            control_frame,
            textvariable=self.time_text
        )

        time_label.grid(
            row=0,
            column=4,
            padx=20
        )

        # Speed label
        speed_label = ttk.Label(
            control_frame,
            text="Speed:"
        )

        speed_label.grid(
            row=1,
            column=0,
            pady=10
        )

        # Speed slider
        self.speed_scale = ttk.Scale(
            control_frame,
            from_=0.1,
            to=5.0,
            orient="horizontal",
            variable=self.simulation_speed,
            command=self.set_simulation_speed
        )

        self.speed_scale.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=10,
            sticky="ew"
        )

        # Speed value
        self.speed_value_label = ttk.Label(
            control_frame,
            text="1.0x"
        )

        self.speed_value_label.grid(
            row=1,
            column=4,
            padx=10
        )

    # =========================================================
    # STATISTICS PANEL
    # =========================================================

    def create_statistics_panel(self):
        """
        Create the network statistics panel.
        """

        self.statistics_frame = ttk.LabelFrame(
            self.root,
            text="Network Statistics",
            padding=10
        )

        self.statistics_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.statistics_frame.columnconfigure(
            1,
            weight=1
        )

        # Statistics
        statistics = [
            ("Packets Generated", self.generated_text),
            ("Packets Forwarded", self.forwarded_text),
            ("Packets Delivered", self.delivered_text),
            ("Packets Lost", self.lost_text),
            ("Packet Loss Rate", self.loss_rate_text),
            ("Delivery Rate", self.delivery_rate_text),
            ("Average Delay", self.delay_text),
            ("Throughput", self.throughput_text),
        ]

        for row, (name, variable) in enumerate(statistics):

            label = ttk.Label(
                self.statistics_frame,
                text=name + ":"
            )

            label.grid(
                row=row,
                column=0,
                sticky="w",
                pady=5
            )

            value = ttk.Label(
                self.statistics_frame,
                textvariable=variable
            )

            value.grid(
                row=row,
                column=1,
                sticky="e",
                pady=5
            )

    # =========================================================
    # ACTIVITY PANEL
    # =========================================================

    def create_activity_panel(self):
        """
        Create the recent activity/event panel.
        """

        self.activity_frame = ttk.LabelFrame(
            self.root,
            text="Simulation Activity",
            padding=10
        )

        self.activity_frame.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
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

        # Activity list
        self.activity_list = tk.Listbox(
            self.activity_frame,
            height=20
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

        self.activity_list.config(
            yscrollcommand=scrollbar.set
        )

    # =========================================================
    # UPDATE STATISTICS
    # =========================================================

    def update_statistics(self, metrics):
        """
        Update statistics displayed in the dashboard.

        Parameters:
            metrics:
                Metrics object or dictionary containing
                simulation statistics.
        """

        try:

            if hasattr(metrics, "get_summary"):
                data = metrics.get_summary()

            elif isinstance(metrics, dict):
                data = metrics

            else:
                return

            self.generated_text.set(
                str(data.get("packets_generated", 0))
            )

            self.forwarded_text.set(
                str(data.get("packets_forwarded", 0))
            )

            self.delivered_text.set(
                str(data.get("packets_delivered", 0))
            )

            self.lost_text.set(
                str(data.get("packets_lost", 0))
            )

            loss_rate = data.get(
                "packet_loss",
                data.get("packet_loss_rate", 0)
            )

            delivery_rate = data.get(
                "delivery_rate",
                0
            )

            self.loss_rate_text.set(
                self._format_percentage(loss_rate)
            )

            self.delivery_rate_text.set(
                self._format_percentage(delivery_rate)
            )

            self.delay_text.set(
                self._format_number(
                    data.get("average_delay", 0)
                )
            )

            self.throughput_text.set(
                self._format_number(
                    data.get("throughput", 0)
                )
            )

        except Exception as error:

            print(
                "Error updating statistics:",
                error
            )

    # =========================================================
    # UPDATE ACTIVITY
    # =========================================================

    def update_activity(self, event):
        """
        Add an event to the activity list.

        Parameters:
            event:
                Event information. Can be a string,
                dictionary, or object.
        """

        if self.activity_list is None:
            return

        if isinstance(event, str):

            message = event

        elif isinstance(event, dict):

            message = event.get(
                "message",
                str(event)
            )

        else:

            if hasattr(event, "message"):

                message = str(
                    event.message
                )

            else:

                message = str(event)

        self.activity_list.insert(
            tk.END,
            message
        )

        # Keep the latest event visible
        self.activity_list.see(
            tk.END
        )

        # Prevent unlimited GUI entries
        max_entries = 200

        if self.activity_list.size() > max_entries:

            self.activity_list.delete(
                0,
                self.activity_list.size()
                - max_entries
            )

    # =========================================================
    # START SIMULATION
    # =========================================================

    def start_simulation(self):
        """
        Start or resume the simulation.
        """

        try:

            if hasattr(
                self.simulation,
                "start_simulation"
            ):

                self.simulation.start_simulation()

            self.status_text.set(
                "Simulation: Running"
            )

            self.start_button.config(
                state="disabled"
            )

            self.pause_button.config(
                state="normal"
            )

            self.update_activity(
                "Simulation started."
            )

            self.refresh()

        except Exception as error:

            print(
                "Error starting simulation:",
                error
            )

    # =========================================================
    # PAUSE SIMULATION
    # =========================================================

    def pause_simulation(self):
        """
        Pause the simulation.
        """

        try:

            if hasattr(
                self.simulation,
                "pause_simulation"
            ):

                self.simulation.pause_simulation()

            self.status_text.set(
                "Simulation: Paused"
            )

            self.start_button.config(
                state="normal"
            )

            self.pause_button.config(
                state="disabled"
            )

            self.update_activity(
                "Simulation paused."
            )

        except Exception as error:

            print(
                "Error pausing simulation:",
                error
            )

    # =========================================================
    # RESET SIMULATION
    # =========================================================

    def reset_simulation(self):
        """
        Reset the simulation to its initial state.
        """

        try:

            if hasattr(
                self.simulation,
                "reset_simulation"
            ):

                self.simulation.reset_simulation()

            self.status_text.set(
                "Simulation: Stopped"
            )

            self.time_text.set(
                "Simulation Time: 0"
            )

            self.start_button.config(
                state="normal"
            )

            self.pause_button.config(
                state="disabled"
            )

            # Reset displayed statistics
            self.generated_text.set("0")
            self.forwarded_text.set("0")
            self.delivered_text.set("0")
            self.lost_text.set("0")
            self.loss_rate_text.set("0%")
            self.delivery_rate_text.set("0%")
            self.delay_text.set("0")
            self.throughput_text.set("0")

            # Clear activity
            if self.activity_list is not None:

                self.activity_list.delete(
                    0,
                    tk.END
                )

            self.update_activity(
                "Simulation reset."
            )

        except Exception as error:

            print(
                "Error resetting simulation:",
                error
            )

    # =========================================================
    # SET SIMULATION SPEED
    # =========================================================

    def set_simulation_speed(self, speed):
        """
        Change simulation speed.

        Parameters:
            speed:
                Speed value received from the Tkinter scale.
        """

        try:

            speed = float(speed)

            self.speed_value_label.config(
                text=f"{speed:.1f}x"
            )

            if hasattr(
                self.simulation,
                "set_simulation_speed"
            ):

                self.simulation.set_simulation_speed(
                    speed
                )

        except ValueError:

            pass

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        """
        Refresh the dashboard with the latest
        simulation state.
        """

        if self.root is None:
            return

        try:

            # Update metrics
            if hasattr(
                self.simulation,
                "metrics"
            ):

                self.update_statistics(
                    self.simulation.metrics
                )

            # Update simulation time
            if hasattr(
                self.simulation,
                "get_simulation_time"
            ):

                simulation_time = (
                    self.simulation
                    .get_simulation_time()
                )

                self.time_text.set(
                    f"Simulation Time: "
                    f"{simulation_time}"
                )

            elif hasattr(
                self.simulation,
                "simulation_time"
            ):

                self.time_text.set(
                    f"Simulation Time: "
                    f"{self.simulation.simulation_time}"
                )

            # Ask simulation to perform an update
            if hasattr(
                self.simulation,
                "update_simulation"
            ):

                running = getattr(
                    self.simulation,
                    "running",
                    False
                )

                paused = getattr(
                    self.simulation,
                    "paused",
                    False
                )

                if running and not paused:

                    self.simulation.update_simulation()

        except Exception as error:

            print(
                "Error refreshing dashboard:",
                error
            )

        # Schedule next refresh
        self.root.after(
            100,
            self.refresh
        )

    # =========================================================
    # RUN
    # =========================================================

    def run(self):
        """
        Start the dashboard application.
        """

        if self.root is None:

            self.create_window()

        # Initial button state
        self.pause_button.config(
            state="disabled"
        )

        # Start GUI refresh cycle
        self.root.after(
            100,
            self.refresh
        )

        # Start Tkinter event loop
        self.root.mainloop()

    # =========================================================
    # CLOSE WINDOW
    # =========================================================

    def _close_window(self):
        """
        Safely close the dashboard.
        """

        try:

            if hasattr(
                self.simulation,
                "pause_simulation"
            ):

                self.simulation.pause_simulation()

        except Exception:
            pass

        if self.root is not None:

            self.root.destroy()

            self.root = None

    # =========================================================
    # FORMATTING HELPERS
    # =========================================================

    @staticmethod
    def _format_percentage(value):
        """
        Format a percentage value.
        """

        try:

            value = float(value)

            # If value is between 0 and 1,
            # treat it as a ratio.
            if 0 <= value <= 1:

                value *= 100

            return f"{value:.2f}%"

        except (ValueError, TypeError):

            return "0%"

    @staticmethod
    def _format_number(value):
        """
        Format numerical statistics.
        """

        try:

            value = float(value)

            return f"{value:.2f}"

        except (ValueError, TypeError):

            return "0"
