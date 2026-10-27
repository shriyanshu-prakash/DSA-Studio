import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.widgets import (
    new_page, page_header, card, muted, button, entry, option_menu, Tabs
)
from algorithms.searching import linear_search, binary_search

NAME = "Searching"


def build(app):
    t = app.theme

    page = new_page(app)
    page_header(page, t, "Searching Lab", INFO[NAME]["subtitle"])
    tabs = Tabs(page, t, TABS, app.tab_memory, NAME)
    attach(tabs, app, NAME)

    viz = tabs.frames["Visualization"]
    panel = card(viz, t)
    panel.pack(fill="x", anchor="n")

    row = tk.Frame(panel, bg=t["panel"])
    row.pack(fill="x", padx=18, pady=18)

    numbers = tk.StringVar(value="2, 4, 6, 8, 10, 12")
    target = tk.StringVar(value="8")
    method = tk.StringVar(value="Binary Search")

    muted(row, t, "Numbers").grid(row=0, column=0, sticky="w")
    entry(row, t, numbers, width=28).grid(
        row=1, column=0, padx=(0, 10), pady=5, ipady=6
    )
    muted(row, t, "Target").grid(row=0, column=1, sticky="w")
    entry(row, t, target, width=10).grid(
        row=1, column=1, padx=(0, 10), pady=5, ipady=6
    )
    option_menu(row, t, method, ["Linear Search", "Binary Search"]).grid(
        row=1, column=2, padx=5
    )
    button(
        row, t, "Search", lambda: search(), "primary", padx=15, pady=8
    ).grid(row=1, column=3, padx=8)

    result = tk.Label(
        panel, text="Results will appear here.", bg=t["panel"],
        fg=t["muted"], font=(FONT, 11), anchor="w"
    )
    result.pack(fill="x", padx=18, pady=(0, 18))

    def search():
        try:
            arr = [
                int(x.strip()) for x in numbers.get().split(",")
                if x.strip()
            ]
            key = int(target.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Enter comma-separated integers and an integer target."
            )
            return

        try:
            if method.get() == "Linear Search":
                index, steps = linear_search(arr, key)
            else:
                index, steps = binary_search(arr, key)
        except ValueError as error:
            messagebox.showerror("Search error", str(error))
            return

        comparisons = sum(1 for step in steps if step[2] == "compare")
        result.configure(
            text=f"{'Found' if index >= 0 else 'Not found'}"
                 f" · Index: {index} · Comparisons: {comparisons}",
            fg=t["text"]
        )

    tabs.start()
