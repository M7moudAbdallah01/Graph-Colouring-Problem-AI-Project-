import tkinter as tk
from tkinter import messagebox
import math


BG = "#111111"
CARD = "#1D1D1D"
CARD2 = "#252525"
RED = "#E82445"
LIGHT_RED = "#D63838"
WHITE = "#FFFFFF"
GRAY = "#D0D0D0"
MUTED = "#999999"
BORDER = "#363636"


class ParameterTuning(tk.Frame):
    """Parameter configuration page for GA and MA."""

    def __init__(
        self,
        parent,
        algorithm,
        graph_data,
        on_back=None,
        on_run=None
    ):
        super().__init__(parent, bg=BG)

        self.algorithm = algorithm
        self.graph_data = graph_data or {}
        self.on_back = on_back
        self.on_run = on_run

        # Default algorithm parameters
        is_genetic = algorithm == "Genetic Algorithm"

        self.population_var = tk.StringVar(
            value="80" if is_genetic else "70"
        )

        self.generations_var = tk.StringVar(
            value="250" if is_genetic else "180"
        )

        self.mutation_var = tk.StringVar(
            value="0.08" if is_genetic else "0.07"
        )

        self.local_steps_var = tk.StringVar(value="35")

        self.build_ui()

    # ==========================================
    # UI
    # ==========================================

    def build_ui(self):

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=22, pady=(12, 5))

        tk.Label(
            header,
            text="◈  AI PROJECT",
            font=("Arial", 12, "bold"),
            fg=LIGHT_RED,
            bg=BG
        ).pack(side="left")

        tk.Label(
            header,
            text="GRAPH COLORING SOLVER",
            font=("Arial", 8, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="right")

        # Heading
        heading = tk.Frame(self, bg=BG)
        heading.pack(fill="x", padx=24, pady=(4, 10))

        tk.Label(
            heading,
            text="Parameter Tuning",
            font=("Arial", 20, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            heading,
            text=f"Configure {self.algorithm} before running it",
            font=("Arial", 9),
            fg=GRAY,
            bg=BG
        ).pack(anchor="w", pady=(2, 0))

        # Graph Summary
        vertices = self.graph_data.get("vertices", 0)
        edges = len(self.graph_data.get("edges", []))

        summary = tk.Frame(
            self,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        summary.pack(fill="x", padx=22, pady=(0, 12))

        tk.Label(
            summary,
            text=f"CURRENT GRAPH     Vertices: {vertices}     |     Edges: {edges}",
            font=("Arial", 9, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w", padx=14, pady=10)

        # Body
        body = tk.Frame(self, bg=BG)
        body.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 8)
        )

        # Settings
        settings = tk.Frame(
            body,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        settings.pack(fill="x", pady=(0, 10))

        tk.Label(
            settings,
            text="ALGORITHM PARAMETERS",
            font=("Arial", 9, "bold"),
            fg=LIGHT_RED,
            bg=CARD
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=14,
            pady=(12, 8)
        )

        self._field(
            settings,
            "Population Size",
            self.population_var,
            1,
            "Number of candidate solutions in each generation."
        )

        self._field(
            settings,
            "Generations",
            self.generations_var,
            2,
            "Maximum number of evolutionary iterations."
        )

        self._field(
            settings,
            "Mutation Rate (0 - 1)",
            self.mutation_var,
            3,
            "Probability of mutation for each individual gene."
        )

        if self.algorithm == "Memetic Algorithm":

            self._field(
                settings,
                "Local Search Steps",
                self.local_steps_var,
                4,
                "Number of local improvement attempts."
            )

        settings.grid_columnconfigure(1, weight=1)

        # Footer
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=22, pady=(0, 10))

        self._button(
            footer,
            "← Back",
            self.go_back,
            bg=CARD2,
            active="#383838"
        ).pack(side="left", ipadx=12, ipady=6)

        self._button(
            footer,
            "Run Algorithm  →",
            self.run
        ).pack(side="right", ipadx=16, ipady=6)

    # ==========================================
    # INPUT FIELD
    # ==========================================

    def _field(self, parent, label, variable, row, help_text):

        tk.Label(
            parent,
            text=label,
            font=("Arial", 9, "bold"),
            fg=GRAY,
            bg=CARD
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=14,
            pady=7
        )

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 9),
            fg=WHITE,
            bg="#121212",
            insertbackground=WHITE,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=RED,
            width=18
        )

        entry.grid(
            row=row,
            column=1,
            sticky="w",
            padx=(8, 14),
            pady=7,
            ipady=5
        )

        tk.Label(
            parent,
            text=help_text,
            font=("Arial", 8),
            fg=MUTED,
            bg=CARD
        ).grid(
            row=row,
            column=2,
            sticky="w",
            padx=(0, 12),
            pady=7
        )

    # ==========================================
    # BUTTON
    # ==========================================

    def _button(
        self,
        parent,
        text,
        command,
        bg=RED,
        active=LIGHT_RED
    ):

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
    # NAVIGATION
    # ==========================================

    def go_back(self):

        if callable(self.on_back):
            self.on_back()

    # ==========================================
    # VALIDATION
    # ==========================================

    def validate_parameters(self):

        try:
            population = int(self.population_var.get().strip())
            generations = int(self.generations_var.get().strip())
            mutation = float(self.mutation_var.get().strip())

            if not 10 <= population <= 2000:
                raise ValueError(
                    "Population Size must be between 10 and 2000."
                )

            if not 1 <= generations <= 10000:
                raise ValueError(
                    "Generations must be between 1 and 10000."
                )

            if not math.isfinite(mutation):
                raise ValueError(
                    "Mutation Rate must be a finite number."
                )

            if not 0.0 <= mutation <= 1.0:
                raise ValueError(
                    "Mutation Rate must be between 0 and 1."
                )

            params = {
                "population_size": population,
                "generations": generations,
                "mutation_rate": mutation
            }

            if self.algorithm == "Memetic Algorithm":

                local_steps = int(
                    self.local_steps_var.get().strip()
                )

                if not 1 <= local_steps <= 1000:
                    raise ValueError(
                        "Local Search Steps must be between 1 and 1000."
                    )

                params["local_steps"] = local_steps

            return params

        except ValueError as error:
            raise ValueError(str(error))

    # ==========================================
    # RUN ALGORITHM
    # ==========================================

    def run(self):

        try:
            params = self.validate_parameters()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Parameters",
                str(error),
                parent=self
            )

            return

        if callable(self.on_run):

            self.on_run(
                self.algorithm,
                self.graph_data,
                params
            )

        else:

            messagebox.showwarning(
                "Algorithm Not Connected",
                "No algorithm execution callback is connected.",
                parent=self
            )