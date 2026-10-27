import tkinter as tk

from ui.theme import FONT
from ui.content import INFO
from ui.widgets import card, chip


def _height(node):
    return 0 if node is None else 1 + max(_height(node.left), _height(node.right))


def stats_for(app, name):
    """Live numbers shown at the top of the Analysis tab."""
    m = app.models.get(name)
    dash = "—"

    if name == "Stack":
        v = m.values()
        return [("Size", len(v)), ("Top", v[-1] if v else dash)]
    if name == "Queue":
        v = m.values()
        return [("Size", len(v)), ("Front", v[0] if v else dash),
                ("Rear", v[-1] if v else dash)]
    if name == "Linked List":
        v = m.values()
        return [("Length", len(v)), ("Head", v[0] if v else dash),
                ("Tail", v[-1] if v else dash)]
    if name == "Binary Search Tree":
        v = m.inorder()
        return [("Nodes", len(v)), ("Height", _height(m.root)),
                ("Min", v[0] if v else dash), ("Max", v[-1] if v else dash)]
    if name == "AVL Tree":
        return [("Nodes", m.size()), ("Height", m.tree_height()),
                ("Rotations", len(m.rotations)),
                ("Root", m.root.value if m.root else dash)]
    if name == "B-Tree":
        v = m.inorder()
        return [("Keys", len(v)), ("Min", v[0] if v else dash),
                ("Max", v[-1] if v else dash)]
    if name == "Heap":
        v = m.items
        return [("Size", len(v)), ("Minimum", v[0] if v else dash)]
    if name == "Sorting":
        s = app.sort_state
        steps = s["steps"]
        return [("Algorithm", s["method"]), ("Steps", len(steps))]
    if name == "Graph Lab":
        adj = m.adjacency
        edges = {tuple(sorted((a, b))) for a, es in adj.items() for b, _ in es}
        return [("Vertices", len(adj)), ("Edges", len(edges))]
    return []


def _clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def _analysis(frame, t, name, stats):
    _clear(frame)

    if stats:
        row = tk.Frame(frame, bg=t["bg"])
        row.pack(fill="x", pady=(0, 14))
        for i, (label, value) in enumerate(stats):
            row.grid_columnconfigure(i, weight=1, uniform="stat")
            tile = card(row, t)
            tile.grid(
                row=0, column=i, sticky="nsew",
                padx=(0 if i == 0 else 7, 0 if i == len(stats) - 1 else 7)
            )
            tk.Label(
                tile, text=label, bg=t["panel"], fg=t["muted"],
                font=(FONT, 9), anchor="w"
            ).pack(fill="x", padx=16, pady=(14, 0))
            tk.Label(
                tile, text=str(value), bg=t["panel"], fg=t["text"],
                font=(FONT, 18, "bold"), anchor="w"
            ).pack(fill="x", padx=16, pady=(2, 14))

    box = card(frame, t, "Time and space complexity")
    box.pack(fill="x")
    for operation, cost in INFO[name]["complexity"]:
        row = tk.Frame(box, bg=t["panel"])
        row.pack(fill="x", padx=16, pady=4)
        tk.Label(
            row, text=operation, bg=t["panel"], fg=t["text"],
            font=(FONT, 10)
        ).pack(side="left")
        chip(row, t, cost).pack(side="right")
    tk.Frame(box, height=10, bg=t["panel"]).pack()


def _wrapped(parent, t, text, **kw):
    label = tk.Label(
        parent, text=text, bg=t["panel"], justify="left", anchor="w", **kw
    )
    label.bind(
        "<Configure>",
        lambda e: label.configure(wraplength=max(200, e.width - 4))
    )
    return label


def _explanation(frame, t, name):
    _clear(frame)
    info = INFO[name]

    how = card(frame, t, "How it works")
    how.pack(fill="x", pady=(0, 14))
    for paragraph in info["explanation"]:
        _wrapped(
            how, t, paragraph, fg=t["text"], font=(FONT, 10)
        ).pack(fill="x", padx=16, pady=(0, 10))

    props = card(frame, t, "Key properties")
    props.pack(fill="x")
    for line in info["properties"]:
        _wrapped(
            props, t, f"•  {line}", fg=t["text"], font=(FONT, 10)
        ).pack(fill="x", padx=16, pady=(0, 6))
    tk.Frame(props, height=6, bg=t["panel"]).pack()


def attach(tabs, app, name):
    """Wire the Analysis and Explanation tabs for a page."""
    t = app.theme
    tabs.on_show["Analysis"] = (
        lambda f: _analysis(f, t, name, stats_for(app, name))
    )
    tabs.on_show["Explanation"] = lambda f: _explanation(f, t, name)
