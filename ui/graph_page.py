import math
import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.widgets import (
    new_page, page_header, card, muted, button, entry, Tabs, Viewport
)

NAME = "Graph Lab"


def build(app):
    t = app.theme
    st = app.state.setdefault(NAME, {"order": None, "text": ""})

    def graph():
        return app.models[NAME]

    page = new_page(app)
    page_header(page, t, NAME, INFO[NAME]["subtitle"])
    tabs = Tabs(page, t, TABS, app.tab_memory, NAME)
    attach(tabs, app, NAME)

    viz = tabs.frames["Visualization"]
    viz.grid_columnconfigure(1, weight=1)
    viz.grid_rowconfigure(0, weight=1)

    left = tk.Frame(viz, bg=t["bg"], width=300)
    left.grid(row=0, column=0, sticky="ns", padx=(0, 16))
    left.pack_propagate(False)

    u = tk.StringVar(value="A")
    v = tk.StringVar(value="B")
    weight = tk.StringVar(value="1")

    # ---- Add edge ----
    box = card(left, t, "Add Edge")
    box.pack(fill="x", pady=(0, 14))
    for label, variable in [
        ("From vertex  (also the start vertex)", u),
        ("To vertex", v), ("Weight", weight)
    ]:
        muted(box, t, label).pack(fill="x", padx=16, pady=(4, 2))
        entry(box, t, variable).pack(fill="x", padx=16, ipady=6)
    button(
        box, t, "Add edge", lambda: add_edge(), "primary", pady=8
    ).pack(fill="x", padx=16, pady=(14, 16))

    # ---- Algorithms ----
    algo = card(left, t, "Run Algorithm")
    algo.pack(fill="x", pady=(0, 14))
    algo_row = tk.Frame(algo, bg=t["panel"])
    algo_row.pack(fill="x", padx=16, pady=(0, 16))
    names = ["BFS", "DFS", "Dijkstra"]
    for i, name in enumerate(names):
        algo_row.grid_columnconfigure(i, weight=1, uniform="algo")
        button(
            algo_row, t, name, lambda n=name: run_algorithm(n), "soft",
            padx=4, pady=7
        ).grid(row=0, column=i, sticky="ew",
               padx=(0 if i == 0 else 3, 0 if i == 2 else 3))
    button(
        algo, t, "Clear graph", lambda: clear_graph(), "danger", pady=7
    ).pack(fill="x", padx=16, pady=(0, 16))

    # ---- Result ----
    res = card(left, t, "Result")
    res.pack(fill="x")
    result = tk.Label(
        res, text=st["text"] or "Add edges to create a graph.",
        bg=t["panel"], fg=t["muted"], font=(FONT, 9), wraplength=260,
        justify="left", anchor="w"
    )
    result.pack(fill="x", padx=16, pady=(0, 16))

    # ---- canvas ----
    def draw(view):
        c = view.canvas
        adj = graph().adjacency
        vertices = list(adj)
        order = st["order"]

        if not vertices:
            view.empty("Add edges to visualize your graph")
            return

        w, h = view.w, view.h
        coords = {
            node: (
                w / 2 + min(w, h) * .32 * math.cos(2 * math.pi * i / len(vertices)),
                h / 2 + min(w, h) * .32 * math.sin(2 * math.pi * i / len(vertices))
            )
            for i, node in enumerate(vertices)
        }

        seen = set()
        for a, edges in adj.items():
            for b, wt in edges:
                edge = tuple(sorted((a, b)))
                if edge in seen:
                    continue
                seen.add(edge)

                x1, y1 = view.tx(*coords[a])
                x2, y2 = view.tx(*coords[b])
                c.create_line(
                    x1, y1, x2, y2, fill=t["muted"],
                    width=max(1, 2 * view.s)
                )
                c.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, text=str(wt),
                    fill=t["text"], font=view.font(10, "normal")
                )

        r = 22 * view.s
        for node, pos in coords.items():
            x, y = view.tx(*pos)
            c.create_oval(
                x - r, y - r, x + r, y + r, outline="",
                fill=t["accent"] if order and node in order else t["node"]
            )
            c.create_text(
                x, y, text=str(node), fill="white", font=view.font(11)
            )

    view = Viewport(viz, t, draw)
    view.canvas.grid(row=0, column=1, sticky="nsew")

    # ---- behaviour ----
    def show(text):
        st["text"] = text
        result.configure(text=text, fg=t["text"])

    def add_edge():
        try:
            a, b = u.get().strip(), v.get().strip()
            wt = float(weight.get())

            if not a or not b:
                raise ValueError("Enter both vertices.")
            if wt < 0:
                raise ValueError("Use nonnegative weights for this project.")

            graph().add_edge(a, b, wt)
            st["order"] = None
            show(f"Added edge {a} — {b}, weight {wt:g}")
            view.redraw()

        except ValueError as error:
            messagebox.showerror("Invalid edge", str(error))

    def run_algorithm(kind):
        g = graph()
        if not g.adjacency:
            messagebox.showinfo("Empty graph", "Add an edge first.")
            return

        start = u.get().strip()

        try:
            if kind == "BFS":
                order = g.bfs(start)
                text = "BFS: " + " → ".join(order)

            elif kind == "DFS":
                order = g.dfs(start)
                text = "DFS: " + " → ".join(order)

            else:
                distances = g.dijkstra(start)
                order = [
                    n for n, d in distances.items() if d < float("inf")
                ]
                text = "Dijkstra: " + ", ".join(
                    f"{n}: {d:g}" if d < float("inf") else f"{n}: ∞"
                    for n, d in distances.items()
                )

            st["order"] = order
            show(text)
            view.redraw()

        except ValueError as error:
            messagebox.showerror("Graph error", str(error))

    def clear_graph():
        app.reset(NAME)
        st.update(order=None, text="")
        result.configure(text="Add edges to create a graph.", fg=t["muted"])
        view.redraw()

    tabs.start()
