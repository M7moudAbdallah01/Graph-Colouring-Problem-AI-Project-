import tkinter as tk
from tkinter import messagebox
import time


from GUI.dashboard import Dashboard
from GUI.graph_input import GraphInput
from GUI.choose_algorithm import ChooseAlgorithm
from GUI.parameter_tuning import ParameterTuning
from GUI.results import Results


# ==========================================
# COMPARISON PAGE
# ==========================================

class ComparisonPage(tk.Frame):

    BG = "#111111"
    PANEL = "#1B1B1B"
    RED = "#E82445"
    LIGHT_RED = "#D63838"
    WHITE = "#FFFFFF"
    GRAY = "#D0D0D0"
    MUTED = "#999999"

    def __init__(
        self,
        parent,
        comparison,
        on_back=None,
        on_run_another=None,
        on_new_graph=None
    ):
        super().__init__(parent, bg=self.BG)

        self.comparison = comparison or {}
        self.on_back = on_back
        self.on_run_another = on_run_another
        self.on_new_graph = on_new_graph

        self.create_widgets()

    def create_widgets(self):

        # Header
        header = tk.Frame(self, bg=self.BG)
        header.pack(fill="x", padx=30, pady=(22, 15))

        tk.Label(
            header,
            text="ALGORITHMS COMPARISON",
            font=("Arial", 20, "bold"),
            fg=self.WHITE,
            bg=self.BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Compare the results of algorithms on the same graph",
            font=("Arial", 10),
            fg=self.GRAY,
            bg=self.BG
        ).pack(anchor="w", pady=(5, 0))

        # Main panel
        panel = tk.Frame(
            self,
            bg=self.PANEL,
            highlightbackground="#333333",
            highlightthickness=1
        )
        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        if not self.comparison:
            tk.Label(
                panel,
                text="No comparison results available yet.",
                font=("Arial", 13, "bold"),
                fg=self.WHITE,
                bg=self.PANEL
            ).pack(pady=(75, 10))

            tk.Label(
                panel,
                text="Run another algorithm on the same graph to compare results.",
                font=("Arial", 10),
                fg=self.GRAY,
                bg=self.PANEL
            ).pack()

        else:
            self.create_comparison_table(panel)

        # Footer buttons
        footer = tk.Frame(self, bg=self.BG)
        footer.pack(fill="x", padx=30, pady=(0, 20))

        tk.Button(
            footer,
            text="Back to Results",
            command=self.go_back,
            bg="#333333",
            fg=self.WHITE,
            activebackground="#444444",
            activeforeground=self.WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="left")

        tk.Button(
            footer,
            text="New Graph",
            command=self.go_new_graph,
            bg="#333333",
            fg=self.WHITE,
            activebackground="#444444",
            activeforeground=self.WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="right")

        tk.Button(
            footer,
            text="Run Another Algorithm",
            command=self.go_run_another,
            bg=self.RED,
            fg=self.WHITE,
            activebackground=self.LIGHT_RED,
            activeforeground=self.WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="right", padx=10)

    def create_comparison_table(self, parent):

        table = tk.Frame(parent, bg=self.PANEL)
        table.pack(fill="x", padx=18, pady=(20, 10))

        columns = [
            ("Algorithm", 24),
            ("Status", 12),
            ("Colors", 10),
            ("Execution Time", 18)
        ]

        for column, (title, width) in enumerate(columns):
            table.grid_columnconfigure(column, weight=width)

            tk.Label(
                table,
                text=title,
                font=("Arial", 9, "bold"),
                fg=self.RED,
                bg=self.PANEL,
                anchor="w"
            ).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=5,
                pady=(0, 12)
            )

        valid_results = []

        for algorithm, result in self.comparison.items():

            if not isinstance(result, dict):
                continue

            success = result.get("success", False)
            chromatic_number = result.get("chromatic_number")
            execution_time = result.get("execution_time", 0)
            pending = result.get("pending", False)

            if success:
                status = "Success"
            elif pending:
                status = "Pending"
            else:
                status = "Failed"

            colors = (
                str(chromatic_number)
                if success and chromatic_number is not None
                else "-"
            )

            try:
                execution_text = f"{float(execution_time):.6f} s"
            except (TypeError, ValueError):
                execution_text = "-"

            row = len(valid_results) + 1

            values = [
                algorithm,
                status,
                colors,
                execution_text
            ]

            for column, value in enumerate(values):

                color = self.WHITE

                if column == 1:
                    if success:
                        color = "#55CC88"
                    elif pending:
                        color = self.MUTED
                    else:
                        color = self.RED

                tk.Label(
                    table,
                    text=value,
                    font=("Arial", 9),
                    fg=color,
                    bg=self.PANEL,
                    anchor="w"
                ).grid(
                    row=row,
                    column=column,
                    sticky="ew",
                    padx=5,
                    pady=12
                )

            if (
                success
                and isinstance(chromatic_number, int)
                and isinstance(execution_time, (int, float))
            ):
                valid_results.append(
                    (
                        chromatic_number,
                        execution_time,
                        algorithm
                    )
                )

            tk.Frame(
                table,
                bg="#333333",
                height=1
            ).grid(
                row=row + 1,
                column=0,
                columnspan=4,
                sticky="ew",
                pady=(0, 5)
            )

        if not valid_results:
            return

        best = min(valid_results)

        best_frame = tk.Frame(
            parent,
            bg="#252525",
            highlightbackground=self.RED,
            highlightthickness=1
        )
        best_frame.pack(
            fill="x",
            padx=18,
            pady=(25, 10)
        )

        tk.Label(
            best_frame,
            text="BEST RESULT",
            font=("Arial", 9, "bold"),
            fg=self.RED,
            bg="#252525"
        ).pack(anchor="w", padx=15, pady=(12, 5))

        tk.Label(
            best_frame,
            text=best[2],
            font=("Arial", 13, "bold"),
            fg=self.WHITE,
            bg="#252525"
        ).pack(anchor="w", padx=15)

        tk.Label(
            best_frame,
            text=(
                f"Colors: {best[0]}     "
                f"Execution Time: {best[1]:.6f} s"
            ),
            font=("Arial", 9),
            fg=self.GRAY,
            bg="#252525"
        ).pack(anchor="w", padx=15, pady=(5, 12))

    def go_back(self):
        if self.on_back:
            self.on_back()

    def go_run_another(self):
        if self.on_run_another:
            self.on_run_another()

    def go_new_graph(self):
        if self.on_new_graph:
            self.on_new_graph()


# ==========================================
# MAIN APPLICATION
# ==========================================

class GraphColoringApp(tk.Tk):

    ALGORITHMS = (
        "Backtracking Search",
        "Genetic Algorithm",
        "Memetic Algorithm"
    )

    def __init__(self):
        super().__init__()

        self.title("Graph Coloring Problem Solver")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg="#111111")

        # Current navigation state
        self.current_page = None

        self.dashboard_page = None
        self.graph_input_page = None
        self.algorithm_page = None
        self.parameter_page = None
        self.results_page = None
        self.comparison_page = None

        # Application data
        self.graph_data = None
        self.selected_algorithm = None
        self.algorithm_result = None
        self.algorithm_params = {}

        self.comparison = {}

        # Registered algorithm implementations
        self.algorithm_runners = {}

        self.center_window()
        self.show_dashboard()

    # ==========================================
    # WINDOW MANAGEMENT
    # ==========================================

    def center_window(self):
        self.update_idletasks()

        width = 900
        height = 600

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    # ==========================================
    # PAGE MANAGEMENT
    # ==========================================

    def hide_current_page(self):
        if self.current_page is not None:
            self.current_page.pack_forget()

    def show_page(self, page):
        if page is None:
            return

        self.hide_current_page()

        self.current_page = page
        self.current_page.pack(fill="both", expand=True)

    def destroy_page(self, attribute):
        page = getattr(self, attribute, None)

        if page is not None:
            if page == self.current_page:
                self.current_page = None

            page.destroy()
            setattr(self, attribute, None)

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self):
        if self.dashboard_page is None:
            self.dashboard_page = Dashboard(
                self,
                on_continue=self.show_graph_input
            )

        self.show_page(self.dashboard_page)

    # ==========================================
    # GRAPH INPUT
    # ==========================================

    def show_graph_input(self):
        if self.graph_input_page is None:
            self.graph_input_page = GraphInput(
                self,
                on_back=self.show_dashboard,
                on_next=self.show_algorithm_selection
            )

        self.show_page(self.graph_input_page)

    def return_to_graph_input(self):
        self.destroy_page("parameter_page")
        self.destroy_page("results_page")
        self.destroy_page("comparison_page")

        if self.graph_input_page is not None:
            self.show_page(self.graph_input_page)
        else:
            self.show_graph_input()

    # ==========================================
    # ALGORITHM SELECTION
    # ==========================================

    def show_algorithm_selection(
        self,
        graph_data,
        reset_comparison=True
    ):
        self.graph_data = graph_data

        self.destroy_page("parameter_page")
        self.destroy_page("results_page")
        self.destroy_page("comparison_page")
        self.destroy_page("algorithm_page")

        if reset_comparison:
            self.comparison = {}

        self.algorithm_page = ChooseAlgorithm(
            self,
            graph_data=self.graph_data,
            on_back=self.return_to_graph_input,
            on_solve=self.run_selected_algorithm
        )

        self.show_page(self.algorithm_page)

    def return_to_algorithm_selection(self):
        self.destroy_page("parameter_page")

        if self.algorithm_page is not None:
            self.show_page(self.algorithm_page)
        else:
            self.show_algorithm_selection(
                self.graph_data,
                reset_comparison=False
            )

    # ==========================================
    # ALGORITHM REGISTRATION
    # ==========================================

    def register_algorithm(self, algorithm, runner):
        """
        Register an algorithm implementation.

        Expected runner signature:
            runner(graph_data, **params)

        Expected result format:
            {
                "success": bool,
                "colors": {vertex: color_index},
                "chromatic_number": int,
                "execution_time": float,
                "statistics": dict
            }
        """

        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        if not callable(runner):
            raise TypeError("Algorithm runner must be callable.")

        self.algorithm_runners[algorithm] = runner

    # ==========================================
    # ALGORITHM ROUTING
    # ==========================================

    def run_selected_algorithm(self, algorithm, graph_data):
        self.selected_algorithm = algorithm
        self.graph_data = graph_data

        self.algorithm_result = None

        if algorithm not in self.ALGORITHMS:
            messagebox.showerror(
                "Invalid Algorithm",
                f"Unknown algorithm: {algorithm}",
                parent=self
            )
            return

        if algorithm in (
            "Genetic Algorithm",
            "Memetic Algorithm"
        ):
            self.show_parameter_tuning()

        else:
            self.execute_algorithm(
                algorithm,
                graph_data,
                params={}
            )

    # ==========================================
    # PARAMETER TUNING
    # ==========================================

    def show_parameter_tuning(self):
        self.destroy_page("parameter_page")
        self.destroy_page("results_page")
        self.destroy_page("comparison_page")

        self.parameter_page = ParameterTuning(
            self,
            algorithm=self.selected_algorithm,
            graph_data=self.graph_data,
            on_back=self.return_to_algorithm_selection,
            on_run=self.execute_algorithm
        )

        self.show_page(self.parameter_page)

    # ==========================================
    # PENDING RESULT (algorithm not connected yet)
    # ==========================================

    def create_pending_result(self, algorithm, params=None):
        """
        Placeholder result used while an algorithm is not connected yet.

        It lets every page open normally: the graph is shown WITHOUT any
        colouring (no colours are assigned) and the status is "Pending".
        """

        statistics = {"status": "Algorithm not connected yet"}

        if params:
            statistics.update(params)

        return {
            "success": False,
            "pending": True,
            "colors": {},
            "chromatic_number": None,
            "execution_time": 0.0,
            "statistics": statistics
        }

    # ==========================================
    # RESULT VALIDATION
    # ==========================================

    def validate_algorithm_result(self, result, graph_data):
        if not isinstance(result, dict):
            raise TypeError(
                "Algorithm must return a dictionary."
            )

        required_fields = (
            "success",
            "colors",
            "chromatic_number",
            "execution_time",
            "statistics"
        )

        missing = [
            field for field in required_fields
            if field not in result
        ]

        if missing:
            raise ValueError(
                f"Missing result fields: {', '.join(missing)}"
            )

        if not isinstance(result["success"], bool):
            raise TypeError("Result success must be a boolean.")

        if not isinstance(result["colors"], dict):
            raise TypeError("Result colors must be a dictionary.")

        if not isinstance(result["statistics"], dict):
            raise TypeError("Result statistics must be a dictionary.")

        elapsed = result["execution_time"]

        if (
            not isinstance(elapsed, (int, float))
            or isinstance(elapsed, bool)
            or elapsed < 0
        ):
            raise ValueError("Invalid execution time.")

        if result["success"]:
            number = result["chromatic_number"]

            if (
                not isinstance(number, int)
                or isinstance(number, bool)
                or number < 1
            ):
                raise ValueError("Invalid chromatic number.")

            colors = result["colors"]
            vertices = set(range(graph_data["vertices"]))

            normalized_colors = {}

            for vertex in vertices:
                color = colors.get(
                    vertex,
                    colors.get(str(vertex))
                )

                if (
                    not isinstance(color, int)
                    or isinstance(color, bool)
                    or color < 0
                ):
                    raise ValueError(
                        f"Missing or invalid color for vertex {vertex}."
                    )

                normalized_colors[vertex] = color

            for u, v in graph_data["edges"]:
                if normalized_colors[u] == normalized_colors[v]:
                    raise ValueError(
                        f"Invalid coloring: vertices {u} and {v} "
                        "have the same color."
                    )

            actual_number = len(set(normalized_colors.values()))

            if actual_number != number:
                raise ValueError(
                    "Chromatic number does not match the number "
                    "of colors used."
                )

            result["colors"] = normalized_colors

        return result

    # ==========================================
    # ALGORITHM EXECUTION
    # ==========================================

    def execute_algorithm(
        self,
        algorithm,
        graph_data,
        params=None
    ):
        self.selected_algorithm = algorithm
        self.graph_data = graph_data
        self.algorithm_params = params or {}

        if algorithm not in self.ALGORITHMS:
            messagebox.showerror(
                "Invalid Algorithm",
                f"Unknown algorithm: {algorithm}",
                parent=self
            )
            return

        self.configure(cursor="watch")
        self.update_idletasks()

        try:
            runner = self.algorithm_runners.get(algorithm)

            if runner is not None:
                started = time.perf_counter()

                result = runner(
                    graph_data,
                    **self.algorithm_params
                )

                if isinstance(result, dict):
                    result["execution_time"] = (
                        time.perf_counter() - started
                    )

            else:
                # TODO: connect the algorithms here.
                # Register each algorithm (for example in main.py) with:
                #     app.register_algorithm("Backtracking Search", fn)
                #     app.register_algorithm("Genetic Algorithm", fn)
                #     app.register_algorithm("Memetic Algorithm", fn)
                # where fn(graph_data, **params) returns the result dict
                # described in register_algorithm().
                # Until then, a pending result is shown: the pages work
                # normally and the graph is displayed without colouring.
                result = self.create_pending_result(
                    algorithm,
                    self.algorithm_params
                )

            result = self.validate_algorithm_result(
                result,
                graph_data
            )

            self.algorithm_result = result

            # Save this algorithm's result for comparison.
            self.comparison[algorithm] = result

            self.show_results(result)

        except Exception as error:
            messagebox.showerror(
                "Algorithm Error",
                f"An error occurred:\n\n{error}",
                parent=self
            )

        finally:
            self.configure(cursor="")

    # ==========================================
    # RESULTS
    # ==========================================

    def show_results(self, result=None):
        self.destroy_page("results_page")

        self.results_page = Results(
            self,
            graph_data=self.graph_data,
            algorithm=self.selected_algorithm,
            result=result,
            comparison=self.comparison,
            on_back=self.return_to_previous_settings,
            on_new_graph=self.start_new_graph,
            on_comparison=self.show_comparison
        )

        self.show_page(self.results_page)

    def return_to_previous_settings(self):
        self.destroy_page("results_page")

        if self.selected_algorithm in (
            "Genetic Algorithm",
            "Memetic Algorithm"
        ):
            self.show_parameter_tuning()

        elif self.algorithm_page is not None:
            self.show_page(self.algorithm_page)

        else:
            self.show_algorithm_selection(
                self.graph_data,
                reset_comparison=False
            )

    # ==========================================
    # COMPARISON
    # ==========================================

    def show_comparison(self):
        self.destroy_page("comparison_page")

        self.comparison_page = ComparisonPage(
            self,
            comparison=self.comparison,
            on_back=self.return_to_results,
            on_run_another=self.return_to_algorithm_selection,
            on_new_graph=self.start_new_graph
        )

        self.show_page(self.comparison_page)

    def return_to_results(self):
        if self.results_page is not None:
            self.show_page(self.results_page)
        else:
            self.show_results(self.algorithm_result)

    # ==========================================
    # NEW GRAPH
    # ==========================================

    def start_new_graph(self):
        self.destroy_page("results_page")
        self.destroy_page("parameter_page")
        self.destroy_page("algorithm_page")
        self.destroy_page("comparison_page")

        self.graph_data = None
        self.selected_algorithm = None
        self.algorithm_result = None
        self.algorithm_params = {}
        self.comparison = {}

        if self.graph_input_page is not None:
            self.graph_input_page.clear_all()

        self.show_graph_input()