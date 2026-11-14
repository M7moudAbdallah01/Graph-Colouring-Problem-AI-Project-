
import tkinter as tk
from tkinter import messagebox


BG = "#111111"
CARD = "#1D1D1D"
CARD2 = "#252525"
RED = "#E82445"
LIGHT_RED = "#D63838"
WHITE = "#FFFFFF"
GRAY = "#D0D0D0"
MUTED = "#999999"
BORDER = "#363636"


class ChooseAlgorithm(tk.Frame):

    ALGORITHMS = [
        (
            "Backtracking Search",
            "Exact search method that explores possible color assignments."
        ),
        (
            "Genetic Algorithm",
            "Population-based optimization inspired by natural selection."
        ),
        (
            "Memetic Algorithm",
            "Genetic search combined with local improvement."
        )
    ]

    def __init__(self, parent, graph_data, on_back=None, on_solve=None):
        super().__init__(parent, bg=BG)

        self.graph_data = graph_data or {}
        self.on_back = on_back
        self.on_solve = on_solve

        self.selected_algorithm = tk.StringVar(
            value="Backtracking Search"
        )

        self.algorithm_cards = {}

        self.build_ui()

    # ==========================================
    # BUTTON
    # ==========================================

    def button(self, parent, text, command, bg=RED, active=LIGHT_RED):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 9, "bold"),
            fg=WHITE,
            bg=bg,
            activebackground=active,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=25, pady=(15, 8))

        tk.Label(
            header,
            text="◈  AI PROJECT",
            font=("Arial", 13, "bold"),
            fg=LIGHT_RED,
            bg=BG
        ).pack(side="left")

        tk.Label(
            header,
            text="GRAPH COLORING SOLVER",
            font=("Arial", 9, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="right")

        # Heading
        tk.Label(
            self,
            text="Choose Algorithm",
            font=("Arial", 21, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(anchor="w", padx=27, pady=(10, 4))

        tk.Label(
            self,
            text="Select the method you want to use to solve the graph",
            font=("Arial", 10),
            fg=GRAY,
            bg=BG
        ).pack(anchor="w", padx=27)

        # Graph Information
        info = tk.Frame(
            self,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        info.pack(fill="x", padx=27, pady=(18, 14))

        vertices = self.graph_data.get("vertices", 0)
        edges = len(self.graph_data.get("edges", []))

        tk.Label(
            info,
            text=(
                f"Current Graph    •    "
                f"{vertices} Vertices    •    {edges} Edges"
            ),
            font=("Arial", 9, "bold"),
            fg=GRAY,
            bg=CARD
        ).pack(anchor="w", padx=14, pady=10)

        # Algorithm Cards
        cards = tk.Frame(self, bg=BG)
        cards.pack(
            fill="both",
            expand=True,
            padx=27,
            pady=(0, 10)
        )

        for name, description in self.ALGORITHMS:

            card = tk.Frame(
                cards,
                bg=CARD,
                highlightthickness=1,
                highlightbackground=BORDER,
                cursor="hand2"
            )

            card.pack(fill="x", pady=5)

            radio = tk.Radiobutton(
                card,
                text=name,
                variable=self.selected_algorithm,
                value=name,
                command=self.refresh_cards,
                indicatoron=True,
                font=("Arial", 11, "bold"),
                fg=WHITE,
                bg=CARD,
                selectcolor=CARD2,
                activebackground=CARD,
                activeforeground=WHITE,
                cursor="hand2"
            )

            radio.pack(anchor="w", padx=12, pady=(8, 1))

            description_label = tk.Label(
                card,
                text=description,
                font=("Arial", 8),
                fg=MUTED,
                bg=CARD,
                wraplength=700,
                justify="left",
                cursor="hand2"
            )

            description_label.pack(
                anchor="w",
                padx=37,
                pady=(0, 9)
            )

            # Make the complete card clickable
            card.bind(
                "<Button-1>",
                lambda event, value=name: self.choose(value)
            )

            description_label.bind(
                "<Button-1>",
                lambda event, value=name: self.choose(value)
            )

            self.algorithm_cards[name] = card

        self.refresh_cards()

        # Footer
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=27, pady=(0, 13))

        self.button(
            footer,
            "← Back",
            self.go_back,
            bg=CARD2,
            active="#383838"
        ).pack(side="left", ipadx=12, ipady=6)

        self.button(
            footer,
            "Solve  →",
            self.solve
        ).pack(side="right", ipadx=18, ipady=6)

        tk.Label(
            self,
            text="© 2026 - 2027 | Artificial Intelligence Project",
            font=("Arial", 8),
            fg=MUTED,
            bg=BG
        ).pack(pady=(0, 7))

    # ==========================================
    # ALGORITHM SELECTION
    # ==========================================

    def choose(self, algorithm):

        if algorithm not in [
            name for name, description in self.ALGORITHMS
        ]:
            return

        self.selected_algorithm.set(algorithm)
        self.refresh_cards()

    def refresh_cards(self):

        selected = self.selected_algorithm.get()

        for name, card in self.algorithm_cards.items():

            card.configure(
                highlightbackground=(
                    RED if name == selected else BORDER
                )
            )

    # ==========================================
    # NAVIGATION
    # ==========================================

    def go_back(self):

        if callable(self.on_back):
            self.on_back()

    # ==========================================
    # SOLVE
    # ==========================================

    def solve(self):

        algorithm = self.selected_algorithm.get()

        if not algorithm:
            messagebox.showwarning(
                "Algorithm Required",
                "Please select an algorithm.",
                parent=self
            )
            return

        if algorithm not in [
            name for name, description in self.ALGORITHMS
        ]:
            messagebox.showerror(
                "Invalid Selection",
                "Please select a valid algorithm.",
                parent=self
            )
            return

        if callable(self.on_solve):

            self.on_solve(
                algorithm,
                self.graph_data
            )

        else:

            messagebox.showinfo(
                "Selection Saved",
                f"Selected: {algorithm}\n"
                "The algorithm execution will be connected next.",
                parent=self
            )
