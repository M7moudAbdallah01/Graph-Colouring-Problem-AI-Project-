import tkinter as tk
from tkinter import font, messagebox
import re
from GUI.graph_layout import calculate_graph_positions

BG = "#111111"
CARD = "#1D1D1D"
CARD2 = "#252525"
RED = "#E82445"
LIGHT_RED = "#D63838"
WHITE = "#FFFFFF"
GRAY = "#D0D0D0"
MUTED = "#999999"
BORDER = "#363636"
EDGE_COLOR = "#AAB4C3"
VERTEX_OUTLINE = "#FFFFFF"


class GraphInput(tk.Frame):
    def __init__(self, parent, on_back=None, on_next=None):
        super().__init__(parent, bg=BG)
        self.on_back = on_back
        self.on_next = on_next
        self.vertices_count = 0
        self.edges = []
        self.positions = {}
        self.graph_ready = False
        self.title_font = font.Font(family="Arial", size=20, weight="bold")
        self.section_font = font.Font(family="Arial", size=11, weight="bold")
        self.normal_font = font.Font(family="Arial", size=9)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=22, pady=(12, 5))
        tk.Label(header, text="◈  AI PROJECT", font=("Arial", 12, "bold"), fg=LIGHT_RED, bg=BG).pack(side="left")
        tk.Label(header, text="GRAPH COLORING SOLVER", font=("Arial", 8, "bold"), fg=MUTED, bg=BG).pack(side="right")

        heading = tk.Frame(self, bg=BG)
        heading.pack(fill="x", padx=24, pady=(3, 10))
        tk.Label(heading, text="Graph Configuration", font=self.title_font, fg=WHITE, bg=BG).pack(anchor="w")
        tk.Label(heading, text="Enter vertices and edges to create your graph", font=("Arial", 9), fg=GRAY, bg=BG).pack(anchor="w", pady=(2, 0))

        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=22, pady=(0, 8))
        self.build_input_panel(content)
        self.build_preview_panel(content)
        self.build_footer()

    def create_button(self, parent, text, command, bg=RED, active=LIGHT_RED):
        return tk.Button(parent, text=text, command=command, font=("Arial", 9, "bold"),
                         fg=WHITE, bg=bg, activebackground=active, activeforeground=WHITE,
                         relief="flat", bd=0, cursor="hand2")

    def build_input_panel(self, parent):
        panel = tk.Frame(parent, bg=CARD, width=245, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(side="left", fill="y", padx=(0, 10))
        panel.pack_propagate(False)
        tk.Label(panel, text="Graph Details", font=self.section_font, fg=WHITE, bg=CARD).pack(anchor="w", padx=12, pady=(10, 2))
        tk.Label(panel, text="Define your graph", font=("Arial", 8), fg=MUTED, bg=CARD).pack(anchor="w", padx=12, pady=(0, 9))
        tk.Label(panel, text="NUMBER OF VERTICES", font=("Arial", 8, "bold"), fg=GRAY, bg=CARD).pack(anchor="w", padx=12, pady=(0, 4))
        self.vertices_entry = tk.Entry(panel, font=self.normal_font, fg=WHITE, bg="#121212", insertbackground=WHITE,
                                       relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=RED)
        self.vertices_entry.pack(fill="x", padx=12, ipady=5)
        tk.Label(panel, text="EDGES", font=("Arial", 8, "bold"), fg=GRAY, bg=CARD).pack(anchor="w", padx=12, pady=(10, 4))
        self.edges_text = tk.Text(panel, height=4, font=("Consolas", 9), fg=WHITE, bg="#121212", insertbackground=WHITE,
                                  relief="flat", wrap="word", highlightthickness=1, highlightbackground=BORDER,
                                  highlightcolor=RED, padx=7, pady=5)
        self.edges_text.pack(fill="x", padx=12)
        tk.Label(panel, text="Example:  0-1, 0-2, 1-2, 2-3", font=("Arial", 9), fg=MUTED, bg=CARD,
                 wraplength=215, justify="left").pack(anchor="w", padx=12, pady=(5, 8))
        self.create_button(panel, "Generate Graph", self.generate_graph).pack(fill="x", padx=12, ipady=5)
        self.create_button(panel, "Clear All", self.clear_all, bg=CARD2, active="#383838").pack(fill="x", padx=12, pady=(6, 0), ipady=5)
        self.message_label = tk.Label(panel, text="", font=("Arial", 7), fg=RED, bg=CARD, wraplength=215, justify="left")
        self.message_label.pack(anchor="w", padx=12, pady=(6, 0))

    def build_preview_panel(self, parent):
        panel = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(side="left", fill="both", expand=True)
        top = tk.Frame(panel, bg=CARD)
        top.pack(fill="x", padx=11, pady=10)
        tk.Label(top, text="Graph Preview", font=self.section_font, fg=WHITE, bg=CARD).pack(side="left")
        self.status_label = tk.Label(top, text="NO GRAPH", font=("Arial", 7, "bold"), fg=MUTED, bg=CARD)
        self.status_label.pack(side="right")
        self.canvas = tk.Canvas(panel, bg="#151515", highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.summary_label = tk.Label(panel, text="Vertices: 0  |  Edges: 0", font=("Arial", 8), fg=GRAY, bg=CARD)
        self.summary_label.pack(anchor="w", padx=12, pady=(0, 8))
        self.draw_empty_state()

    def parse_graph(self):
        raw_vertices = self.vertices_entry.get().strip()
        if not raw_vertices:
            raise ValueError("Please enter the number of vertices.")
        if not raw_vertices.isdigit():
            raise ValueError("Vertices must be a positive integer.")
        n = int(raw_vertices)
        if not 1 <= n <= 100:
            raise ValueError("Vertices must be between 1 and 100.")

        raw_edges = self.edges_text.get("1.0", "end").strip()
        edges, seen = [], set()
        if raw_edges:
            pattern = r"(\d+)\s*-\s*(\d+)"
            matches = list(re.finditer(pattern, raw_edges))
            remaining = re.sub(pattern, "", raw_edges)
            if re.search(r"[^,\s;]", remaining):
                raise ValueError("Invalid edge format. Use 0-1 format.")
            if not matches and raw_edges:
                raise ValueError("Please enter edges in the form 0-1, or leave this field empty.")
            for match in matches:
                u, v = int(match.group(1)), int(match.group(2))
                if u >= n or v >= n:
                    raise ValueError(f"Vertex numbers must be between 0 and {n - 1}.")
                if u == v:
                    raise ValueError("Self-loops are not allowed.")
                edge = (min(u, v), max(u, v))
                if edge in seen:
                    raise ValueError(f"Duplicate edge: {u}-{v}.")
                seen.add(edge)
                edges.append(edge)
        return n, edges

    def generate_graph(self):
        try:
            n, edges = self.parse_graph()
        except ValueError as error:
            self.graph_ready = False
            self.message_label.config(text=str(error), fg=RED)
            self.status_label.config(text="INVALID INPUT", fg=RED)
            self.draw_empty_state()
            messagebox.showerror("Invalid Graph Input", str(error), parent=self)
            return

        self.vertices_count, self.edges, self.graph_ready = n, edges, True
        self.message_label.config(text="Graph generated successfully!", fg="#55C98A")
        self.status_label.config(text="GRAPH READY", fg="#55C98A")
        self.summary_label.config(text=f"Vertices: {n}  |  Edges: {len(edges)}")
        self.draw_graph()

    def draw_graph(self):
        if not self.graph_ready:
            self.draw_empty_state()
            return
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        width, height = max(self.canvas.winfo_width(), 200), max(self.canvas.winfo_height(), 150)
        radius = 18 if self.vertices_count <= 25 else (13 if self.vertices_count <= 50 else 10)
        self.positions = calculate_graph_positions(self.vertices_count, self.edges, width, height, radius)
        for u, v in self.edges:
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill=EDGE_COLOR, width=2)
        font_size = 10 if self.vertices_count <= 25 else (9 if self.vertices_count <= 50 else 8)
        for vertex, (x, y) in self.positions.items():
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=RED, outline=WHITE, width=2)
            self.canvas.create_text(x, y, text=str(vertex), fill=WHITE, font=("Arial", font_size, "bold"))

    def draw_empty_state(self):
        self.canvas.delete("all")
        cx = max(self.canvas.winfo_width(), 200) / 2
        cy = max(self.canvas.winfo_height(), 150) / 2
        self.canvas.create_text(cx, cy - 10, text="Your graph will appear here", fill="#A0A0A0", font=("Arial", 11, "bold"))
        self.canvas.create_text(cx, cy + 13, text="Generate a graph to see its visualization", fill="#888888", font=("Arial", 8))

    def on_canvas_resize(self, event):
        if self.graph_ready:
            self.draw_graph()
        else:
            self.draw_empty_state()

    def clear_all(self):
        self.vertices_entry.delete(0, "end")
        self.edges_text.delete("1.0", "end")
        self.vertices_count, self.edges, self.positions, self.graph_ready = 0, [], {}, False
        self.message_label.config(text="")
        self.status_label.config(text="NO GRAPH", fg=MUTED)
        self.summary_label.config(text="Vertices: 0  |  Edges: 0")
        self.draw_empty_state()

    def go_next(self):
        try:
            n, edges = self.parse_graph()
        except ValueError as error:
            messagebox.showwarning("Graph Required", str(error), parent=self)
            return
        if not self.graph_ready or n != self.vertices_count or edges != self.edges:
            messagebox.showwarning("Graph Not Updated", "Please click Generate Graph after changing the input.", parent=self)
            return
        adjacency = {v: set() for v in range(n)}

        for u, v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        graph_data = {"vertices": n, "edges": edges.copy(), "adjacency": adjacency}
        if callable(self.on_next):
            self.on_next(graph_data)
        else:
            messagebox.showwarning("Navigation", "Algorithm selection callback is not connected.", parent=self)

    def go_back(self):
        if callable(self.on_back):
            self.on_back()
        else:
            messagebox.showwarning("Navigation", "Dashboard callback was not connected in main.py.", parent=self)

    def build_footer(self):
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=22, pady=(0, 10))
        self.create_button(footer, "← Back", self.go_back, bg=CARD2, active="#383838").pack(side="left", ipadx=12, ipady=5)
        self.create_button(footer, "Next  →", self.go_next).pack(side="right", ipadx=17, ipady=5)
