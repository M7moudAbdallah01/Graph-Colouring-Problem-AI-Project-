import tkinter as tk
from tkinter import font

from GUI.graph_layout import calculate_graph_positions


class Results(tk.Frame):

    BG = "#111111"
    PANEL = "#1B1B1B"
    RED = "#E82445"
    LIGHT_RED = "#D63838"
    WHITE = "#FFFFFF"
    GRAY = "#D0D0D0"
    MUTED = "#999999"
    GREEN = "#2ECC71"

    COLOR_PALETTE = [
        "#E82445", "#3498DB", "#2ECC71", "#F1C40F",
        "#9B59B6", "#E67E22", "#1ABC9C", "#E84393",
        "#34495E", "#7F8C8D"
    ]

    def __init__(
        self,
        parent,
        graph_data,
        algorithm,
        result=None,
        on_back=None,
        on_new_graph=None,
        comparison=None,
        on_comparison=None
    ):
        super().__init__(parent, bg=self.BG)

        self.graph_data = graph_data or {}
        self.algorithm = algorithm
        self.result = result or {}
        self.comparison = comparison or {}

        self.on_back = on_back
        self.on_new_graph = on_new_graph
        self.on_comparison = on_comparison

        vertices_count = self.graph_data.get("vertices", 0)
        self.vertices = list(range(vertices_count))
        self.edges = self.graph_data.get("edges", [])

        self.create_fonts()
        self.create_layout()
        self.update_result()

    def create_fonts(self):
        self.title_font = font.Font(
            family="Arial", size=21, weight="bold"
        )
        self.heading_font = font.Font(
            family="Arial", size=12, weight="bold"
        )
        self.normal_font = font.Font(
            family="Arial", size=10
        )
        self.value_font = font.Font(
            family="Arial", size=11, weight="bold"
        )

    def create_layout(self):
        header = tk.Frame(self, bg=self.BG)
        header.pack(fill="x", padx=28, pady=(18, 12))

        tk.Label(
            header,
            text="ALGORITHM RESULTS",
            font=self.title_font,
            fg=self.WHITE,
            bg=self.BG
        ).pack(side="left")

        content = tk.Frame(self, bg=self.BG)
        content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 12)
        )

        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        self.create_graph_panel(content)
        self.create_summary_panel(content)
        self.create_footer()

    def create_graph_panel(self, parent):
        panel = tk.Frame(parent, bg=self.PANEL)
        panel.grid(
            row=0, column=0, sticky="nsew", padx=(0, 8)
        )

        tk.Label(
            panel,
            text="COLORED GRAPH",
            font=self.heading_font,
            fg=self.RED,
            bg=self.PANEL
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.graph_canvas = tk.Canvas(
            panel,
            bg=self.PANEL,
            highlightthickness=0
        )
        self.graph_canvas.pack(
            fill="both", expand=True, padx=10, pady=(0, 10)
        )
        self.graph_canvas.bind(
            "<Configure>", self.draw_graph
        )

    def create_summary_panel(self, parent):
        panel = tk.Frame(parent, bg=self.PANEL)
        panel.grid(
            row=0, column=1, sticky="nsew", padx=(8, 0)
        )

        tk.Label(
            panel,
            text="EXECUTION SUMMARY",
            font=self.heading_font,
            fg=self.RED,
            bg=self.PANEL
        ).pack(anchor="w", padx=16, pady=(14, 12))

        self.algorithm_value = self.add_info(
            panel, "Algorithm", self.algorithm
        )
        self.status_value = self.add_info(
            panel, "Status", "Not executed"
        )
        self.chromatic_value = self.add_info(
            panel, "Chromatic Number", "-"
        )
        self.colors_value = self.add_info(
            panel, "Colors Used", "-"
        )
        self.time_value = self.add_info(
            panel, "Execution Time", "-"
        )

        tk.Label(
            panel,
            text="ALGORITHM STATISTICS",
            font=self.heading_font,
            fg=self.RED,
            bg=self.PANEL
        ).pack(anchor="w", padx=16, pady=(15, 7))

        self.statistics_frame = tk.Frame(
            panel, bg=self.PANEL
        )
        self.statistics_frame.pack(
            fill="both", expand=True, padx=16, pady=(0, 8)
        )

    def add_info(self, parent, label_text, value_text):
        row = tk.Frame(parent, bg=self.PANEL)
        row.pack(fill="x", padx=16, pady=4)

        tk.Label(
            row,
            text=label_text,
            font=self.normal_font,
            fg=self.GRAY,
            bg=self.PANEL
        ).pack(side="left")

        value = tk.Label(
            row,
            text=str(value_text),
            font=self.value_font,
            fg=self.WHITE,
            bg=self.PANEL
        )
        value.pack(side="right")

        return value

    def create_footer(self):
        footer = tk.Frame(self, bg=self.BG)
        footer.pack(fill="x", padx=28, pady=(0, 18))

        self.create_button(
            footer, "← Back", self.go_back,
            side="left", bg="#333333"
        )

        self.create_button(
            footer, "New Graph", self.go_new_graph,
            side="right", bg="#333333"
        )

        self.create_button(
            footer, "Compare Algorithms",
            self.go_comparison,
            side="right", bg=self.RED
        )

    def create_button(self, parent, text, command, side, bg):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg=bg,
            fg=self.WHITE,
            activebackground=self.LIGHT_RED,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            padx=15,
            pady=9,
            cursor="hand2"
        )
        button.pack(side=side, padx=(8, 0))
        return button

    def update_result(self):
        if not self.result:
            self.status_value.config(text="No result")
            return

        success = self.result.get("success", False)
        colors = self.result.get("colors", {})
        chromatic_number = self.result.get("chromatic_number")
        execution_time = self.result.get("execution_time")
        statistics = self.result.get("statistics", {})

        if success:
            self.status_value.config(text="Success", fg=self.GREEN)
        elif self.result.get("pending", False):
            self.status_value.config(
                text="Not connected", fg=self.MUTED
            )
        else:
            self.status_value.config(text="Failed", fg=self.RED)

        self.chromatic_value.config(
            text=str(chromatic_number)
            if chromatic_number is not None else "-"
        )

        self.colors_value.config(
            text=str(len(set(colors.values())))
            if colors else "-"
        )

        if isinstance(execution_time, (int, float)):
            self.time_value.config(
                text=f"{execution_time:.6f} sec"
            )

        self.display_statistics(statistics)

    def display_statistics(self, statistics):
        for widget in self.statistics_frame.winfo_children():
            widget.destroy()

        if not statistics:
            tk.Label(
                self.statistics_frame,
                text="No statistics available.",
                font=self.normal_font,
                fg=self.MUTED,
                bg=self.PANEL
            ).pack(anchor="w")
            return

        for key, value in statistics.items():
            row = tk.Frame(self.statistics_frame, bg=self.PANEL)
            row.pack(fill="x", pady=3)

            tk.Label(
                row,
                text=str(key).replace("_", " ").title(),
                font=self.normal_font,
                fg=self.GRAY,
                bg=self.PANEL
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=self.normal_font,
                fg=self.WHITE,
                bg=self.PANEL
            ).pack(side="right")

    def draw_graph(self, event=None):
        if not hasattr(self, "graph_canvas"):
            return

        self.graph_canvas.delete("all")

        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()

        if width < 20 or height < 20:
            return

        if not self.vertices:
            self.graph_canvas.create_text(
                width / 2,
                height / 2,
                text="No graph to display",
                fill=self.GRAY,
                font=self.normal_font
            )
            return

        positions = calculate_graph_positions(
            len(self.vertices),
            self.edges,
            width,
            height
        )

        self.draw_edges(positions)
        self.draw_vertices(positions)

    def draw_edges(self, positions):
        for u, v in self.edges:
            if u not in positions or v not in positions:
                continue

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            self.graph_canvas.create_line(
                x1, y1, x2, y2,
                fill="#777777",
                width=2
            )

    def draw_vertices(self, positions):
        colors = self.result.get("colors", {})
        radius = 18

        for vertex in self.vertices:
            if vertex not in positions:
                continue

            x, y = positions[vertex]
            color_index = colors.get(
                vertex, colors.get(str(vertex))
            )

            if isinstance(color_index, int):
                fill = self.COLOR_PALETTE[
                    color_index % len(self.COLOR_PALETTE)
                ]
            elif (
                isinstance(color_index, str)
                and color_index.startswith("#")
            ):
                fill = color_index
            else:
                fill = "#555555"

            self.graph_canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=fill,
                outline=self.WHITE,
                width=1
            )

            self.graph_canvas.create_text(
                x, y,
                text=str(vertex),
                fill=self.WHITE,
                font=("Arial", 10, "bold")
            )

    def go_back(self):
        if callable(self.on_back):
            self.on_back()

    def go_new_graph(self):
        if callable(self.on_new_graph):
            self.on_new_graph()

    def go_comparison(self):
        if callable(self.on_comparison):
            self.on_comparison()