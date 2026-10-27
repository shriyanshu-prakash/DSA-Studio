import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.treeview import draw_tree
from ui.widgets import (
    new_page, page_header, card, muted, button, entry, chip, row_label,
    Tabs, Flow, Viewport
)

NAME = "AVL Tree"
TRAVERSALS = [
    ("In-Order", "In-order"), ("Pre-Order", "Pre-order"),
    ("Post-Order", "Post-order")
]


def build(app):
    t = app.theme
    st = app.state.setdefault(
        NAME, {"highlight": None, "traversal": None}
    )

    def avl():
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

    # ---- Insert Node ----
    box = card(left, t, "Insert Node")
    box.pack(fill="x", pady=(0, 14))
    row = tk.Frame(box, bg=t["panel"])
    row.pack(fill="x", padx=16, pady=(0, 16))
    value = tk.StringVar()
    field = entry(row, t, value, "Enter value")
    field.pack(side="left", fill="x", expand=True, ipady=7)
    button(row, t, "Insert", lambda: insert(), "primary", padx=14, pady=7
           ).pack(side="left", padx=(8, 0))

    # ---- Traversal Controls ----
    ctl = card(left, t, "Traversal Controls")
    ctl.pack(fill="x", pady=(0, 14))
    ctl_row = tk.Frame(ctl, bg=t["panel"])
    ctl_row.pack(fill="x", padx=16, pady=(0, 16))
    buttons = [(label, key, "soft") for label, key in TRAVERSALS]
    buttons.append(("Clear", None, "danger"))
    for i, (label, key, kind) in enumerate(buttons):
        ctl_row.grid_columnconfigure(i, weight=1, uniform="trav")
        command = (
            (lambda: clear_tree()) if key is None
            else (lambda k=key, l=label: traverse(l, k))
        )
        button(
            ctl_row, t, label, command, kind, padx=4, pady=7,
            font=(FONT, 8, "bold" if kind == "danger" else "normal")
        ).grid(
            row=0, column=i, sticky="ew",
            padx=(0 if i == 0 else 3, 0 if i == len(buttons) - 1 else 3)
        )

    # ---- Traversal History ----
    trav = card(left, t, "Traversal History")
    trav.pack(fill="x", pady=(0, 14))
    trav_body = tk.Frame(trav, bg=t["panel"])
    trav_body.pack(fill="x", padx=16, pady=(0, 16))

    # ---- Rotation History ----
    rot = card(left, t, "Rotation History")
    rot.pack(fill="x")
    rot_body = tk.Frame(rot, bg=t["panel"])
    rot_body.pack(fill="x", padx=16, pady=(0, 16))

    # ---- canvas ----
    def draw(view):
        tree = avl()
        if not tree.root:
            view.empty("Your AVL tree will appear here")
            return
        draw_tree(
            view, t, tree.root, highlight=st["highlight"],
            balance=tree.balance
        )

    view = Viewport(viz, t, draw)
    view.canvas.grid(row=0, column=1, sticky="nsew")

    # ---- behaviour ----
    def refresh_traversal():
        for widget in trav_body.winfo_children():
            widget.destroy()
        data = st["traversal"]
        if data is None:
            muted(trav_body, t, "Run a traversal to see the order"
                  ).pack(fill="x")
            return
        label, values = data
        if not values:
            muted(trav_body, t, "Tree is empty").pack(fill="x")
            return
        muted(trav_body, t, label).pack(fill="x", pady=(0, 6))
        flow = Flow(trav_body, t["panel"])
        flow.pack(fill="x")
        for v in values:
            flow.add(chip(flow, t, str(v)))

    def refresh_rotations():
        for widget in rot_body.winfo_children():
            widget.destroy()
        rotations = avl().rotations
        if not rotations:
            muted(rot_body, t, "No rotations yet").pack(fill="x")
            return
        hidden = len(rotations) - 4
        if hidden > 0:
            muted(rot_body, t, f"+ {hidden} earlier").pack(
                fill="x", pady=(0, 4)
            )
        for direction, node_value in rotations[-4:]:
            row_label(
                rot_body, t, f"{direction} rotation at {node_value}",
                warn=True
            ).pack(fill="x", pady=2)

    def insert(event=None):
        try:
            v = int(value.get().strip())
        except ValueError:
            messagebox.showerror("Cannot insert", "Enter an integer.")
            return
        try:
            avl().insert(v)
        except ValueError as error:
            messagebox.showerror("Cannot insert", str(error))
            return
        st["highlight"] = v
        value.set("")
        refresh_rotations()
        view.redraw()

    def traverse(label, key):
        st["traversal"] = (label, avl().traversal(key))
        refresh_traversal()

    def clear_tree():
        app.reset(NAME)
        st.update(highlight=None, traversal=None)
        refresh_traversal()
        refresh_rotations()
        view.redraw()

    field.bind("<Return>", insert)
    refresh_traversal()
    refresh_rotations()
    tabs.start()
