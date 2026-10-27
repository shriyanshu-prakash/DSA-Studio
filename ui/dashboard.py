import tkinter as tk

from ui.theme import FONT
from ui.widgets import new_page, page_header, card, button


def build(app):
    t = app.theme
    page = new_page(app)
    page_header(
        page, t, "Welcome to DSA Studio",
        "Explore data structures and watch algorithms come to life."
    )

    grid = tk.Frame(page, bg=t["bg"])
    grid.pack(fill="x", anchor="n")
    grid.grid_columnconfigure((0, 1), weight=1, uniform="cards")

    cards = [
        ("01", "Linear Structures",
         "Stack, Queue and Linked List", "Data Structures"),
        ("02", "Tree Visualizer",
         "BST, AVL Tree and B-Tree", "AVL Tree"),
        ("03", "Algorithm Lab",
         "Sorting and searching", "Algorithms"),
        ("04", "Graph Lab",
         "BFS, DFS and shortest paths", "Graph Lab")
    ]

    for i, (num, title, desc, destination) in enumerate(cards):
        r, c = divmod(i, 2)
        box = card(grid, t)
        box.grid(row=r, column=c, sticky="nsew", padx=9, pady=9)

        tk.Label(
            box, text=num, bg=t["panel"], fg=t["accent"],
            font=(FONT, 10, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 7))
        tk.Label(
            box, text=title, bg=t["panel"], fg=t["text"],
            font=(FONT, 15, "bold")
        ).pack(anchor="w", padx=20, pady=3)
        tk.Label(
            box, text=desc, bg=t["panel"], fg=t["muted"],
            font=(FONT, 10)
        ).pack(anchor="w", padx=20, pady=3)

        button(
            box, t, "Open visualizer  →",
            lambda d=destination: app.show_page(d), kind="primary",
            font=(FONT, 9), padx=12, pady=8
        ).pack(anchor="w", padx=20, pady=(12, 18))


def category(app, category_name):
    t = app.theme
    page = new_page(app)
    page_header(page, t, category_name, "Choose a module to explore.")

    names = (
        ["Stack", "Queue", "Linked List", "Binary Search Tree",
         "AVL Tree", "B-Tree", "Heap"]
        if category_name == "Data Structures"
        else ["Sorting", "Searching", "Graph Lab"]
    )

    panel = card(page, t)
    panel.pack(fill="x", anchor="n")

    for name in names:
        tk.Button(
            panel, text=f"◇   {name}     →", anchor="w",
            command=lambda n=name: app.show_page(n),
            bg=t["panel"], fg=t["text"], activebackground=t["hover"],
            activeforeground=t["text"], relief="flat", bd=0,
            highlightthickness=0, font=(FONT, 10), padx=20, pady=12,
            cursor="hand2"
        ).pack(fill="x")
