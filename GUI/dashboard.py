import tkinter as tk
from tkinter import font

# ==============================
# Main Window

root = tk.Tk()
root.title("Graph Coloring Problem Solver")

window_width = 900
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#111111")
root.resizable(False, False)

# ==============================
# Colors

BG = "#111111"
CARD = "#1D1D1D"
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

header = tk.Frame(root, bg=BG)
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

main_frame = tk.Frame(root, bg=BG)
main_frame.place(relx=0.5, rely=0.49, anchor="center")

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

def continue_app():
    print("Welcome to Graph Coloring Solver!")

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
    command=continue_app
)

continue_button.pack(pady=30)

# ==============================
# Footer

footer = tk.Label(
    root,
    text="© 2026 - 2027 | Artificial Intelligence Project",
    font=("Arial", 10),
    fg="#999999",
    bg=BG
)

footer.pack(side="bottom", pady=20)

# ==============================
# Run Application

root.mainloop()
