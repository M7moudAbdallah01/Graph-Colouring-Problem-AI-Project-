import tkinter as tk
from tkinter import font


class Dashboard(tk.Frame):

    def __init__(self, master, on_continue):
        super().__init__(master, bg="#111111")

        self.on_continue = on_continue

        # ==============================
        # Colors

        BG = "#111111"
        BLUE = "#E82445"
        LIGHT_BLUE = "#D63838"
        WHITE = "#FFFFFF"
        GRAY = "#D0D0D0"

        # ==============================
        # Fonts

        title_font = font.Font(
            family="Arial",
            size=30,
            weight="bold"
        )

        subtitle_font = font.Font(
            family="Arial",
            size=16,
            weight="bold"
        )

        normal_font = font.Font(
            family="Arial",
            size=12
        )

        # ==============================
        # Header

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=35, pady=25)

        logo = tk.Label(
            header,
            text="◈  AI PROJECT",
            font=("Arial", 14, "bold"),
            fg=LIGHT_BLUE,
            bg=BG
        )
        logo.pack(side="left")

        # ==============================
        # Main Content

        main_frame = tk.Frame(self, bg=BG)
        main_frame.place(
            relx=0.5,
            rely=0.49,
            anchor="center"
        )

        project_title = tk.Label(
            main_frame,
            text="GRAPH COLORING",
            font=title_font,
            fg=WHITE,
            bg=BG
        )
        project_title.pack()

        project_subtitle = tk.Label(
            main_frame,
            text="PROBLEM SOLVER",
            font=subtitle_font,
            fg=LIGHT_BLUE,
            bg=BG
        )
        project_subtitle.pack(pady=5)

        welcome = tk.Label(
            main_frame,
            text="Welcome to our intelligent Graph Coloring Solver",
            font=normal_font,
            fg=GRAY,
            bg=BG
        )
        welcome.pack(pady=(25, 8))

        # ==============================
        # Continue Button

        continue_button = tk.Button(
            main_frame,
            text="Continue  →",
            font=("Arial", 13, "bold"),
            fg=WHITE,
            bg=BLUE,
            activebackground=LIGHT_BLUE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=20,
            height=2,
            command=self.on_continue
        )

        continue_button.pack(pady=30)

        # ==============================
        # Footer

        footer = tk.Label(
            self,
            text="© 2026 - 2027 | Artificial Intelligence Project",
            font=("Arial", 10),
            fg="#999999",
            bg=BG
        )

        footer.pack(side="bottom", pady=20)
