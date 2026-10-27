import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.widgets import (
    new_page, page_header, card, button, entry, option_menu, Tabs, Viewport
)
from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort
)

NAME = "Sorting"
FUNCTIONS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}


def build(app):
    t = app.theme
    st = app.sort_state

    page = new_page(app)
    page_header(page, t, "Sorting Lab", INFO[NAME]["subtitle"])
    tabs = Tabs(page, t, TABS, app.tab_memory, NAME)
    attach(tabs, app, NAME)

    viz = tabs.frames["Visualization"]
    panel = card(viz, t)
    panel.pack(fill="both", expand=True)

    top = tk.Frame(panel, bg=t["panel"])
    top.pack(fill="x", padx=16, pady=(16, 10))

    numbers = tk.StringVar(value=st["values"])
    method = tk.StringVar(value=st["method"])

    entry(top, t, numbers, width=26).pack(
        side="left", padx=(0, 8), ipady=7
    )
    option_menu(top, t, method, list(FUNCTIONS)).pack(side="left")
    button(
        top, t, "Generate steps", lambda: run_sort(), "primary",
        padx=14, pady=8
    ).pack(side="left", padx=8)

    controls = tk.Frame(panel, bg=t["panel"])
    controls.pack(fill="x", padx=16)
    button(controls, t, "◀ Previous", lambda: move(-1), "soft",
           padx=12, pady=7).pack(side="left", padx=(0, 6))
    button(controls, t, "Next ▶", lambda: move(1), "soft",
           padx=12, pady=7).pack(side="left")

    status = tk.Label(
        panel, text="Enter numbers and generate steps.",
        bg=t["panel"], fg=t["muted"], font=(FONT, 10), anchor="w"
    )
    status.pack(fill="x", padx=18, pady=10)

    def draw(view):
        if not st["steps"]:
            view.empty("Enter numbers and generate steps")
            return

        arr, a, b, kind = st["steps"][st["step"]]
        c = view.canvas
        w, h = view.w, view.h
        max_value = max(arr) if arr else 1
        gap = w / (len(arr) + 1)
        bar_width = min(55, gap * .7)

        for i, v in enumerate(arr):
            bar_height = (h - 75) * v / max(1, max_value)
            x = (i + 1) * gap
            color = (
                t["accent"] if i in (a, b) and kind != "complete"
                else t["node"]
            )
            c.create_rectangle(
                x - bar_width / 2, h - 45 - bar_height,
                x + bar_width / 2, h - 45, fill=color, outline=""
            )
            c.create_text(x, h - 28, text=str(v), fill=t["text"],
                          font=(FONT, 10))

        status.configure(
            text=f"Step {st['step'] + 1}/{len(st['steps'])}"
                 f" · {kind.title()} · Array: {arr}"
        )

    view = Viewport(panel, t, draw, controls=False)
    view.canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def run_sort():
        try:
            arr = [
                int(x.strip()) for x in numbers.get().split(",")
                if x.strip()
            ]
            if not arr:
                raise ValueError("Enter at least one number.")
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        sorted_arr, steps = FUNCTIONS[method.get()](arr)
        st["steps"] = steps + [(sorted_arr.copy(), -1, -1, "complete")]
        st["step"] = 0
        st["values"] = numbers.get()
        st["method"] = method.get()
        view.redraw()

    def move(delta):
        if not st["steps"]:
            return
        st["step"] = max(0, min(len(st["steps"]) - 1, st["step"] + delta))
        view.redraw()

    tabs.start()
