import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.treeview import draw_tree
from ui.widgets import (
    new_page, page_header, card, muted, button, entry, row_label,
    Tabs, Viewport
)

CONFIG = {
    "Stack": {"add": "Push", "card": "Push Value", "others": ["Pop"]},
    "Queue": {"add": "Enqueue", "card": "Enqueue Value", "others": ["Dequeue"]},
    "Linked List": {"add": "Insert", "card": "Insert Node",
                    "others": ["Delete", "Search"]},
    "Binary Search Tree": {"add": "Insert", "card": "Insert Node",
                           "others": ["Delete", "Search"]},
    "B-Tree": {"add": "Insert", "card": "Insert Key", "others": ["Search"]},
    "Heap": {"add": "Push", "card": "Push Value", "others": ["Extract min"]},
}


def values_now(app, name):
    m = app.models[name]
    if name in ("Stack", "Queue", "Linked List"):
        return m.values()
    if name in ("Binary Search Tree", "B-Tree"):
        return m.inorder()
    return m.items.copy()


def draw_linear(view, t, name, vals):
    c = view.canvas
    w, h = view.w, view.h
    s = view.s
    boxw = min(90, max(50, (w - 60) / max(1, len(vals))))

    for i, v in enumerate(vals):
        if name == "Stack":
            cx, cy = w / 2, h - 65 - i * 48
            x1, y1 = view.tx(cx - boxw / 2, cy - 20)
            x2, y2 = view.tx(cx + boxw / 2, cy + 20)
        else:
            left = 25 + i * boxw
            x1, y1 = view.tx(left, h / 2 - 22)
            x2, y2 = view.tx(left + boxw - 5, h / 2 + 22)

        c.create_rectangle(
            x1, y1, x2, y2, fill=t["node"], outline=t["border"]
        )
        c.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2, text=str(v),
            fill="white", font=view.font(11)
        )

        if name == "Linked List" and i < len(vals) - 1:
            ax, ay = view.tx(left + boxw - 5, h / 2)
            bx, by = view.tx(left + boxw + 7, h / 2)
            c.create_line(
                ax, ay, bx, by, arrow=tk.LAST,
                fill=t["accent"], width=max(1, 2 * s)
            )


def build(app, name):
    t = app.theme
    cfg = CONFIG[name]
    st = app.state.setdefault(
        name, {"history": [], "status": "Ready", "highlight": None}
    )

    page = new_page(app)
    page_header(page, t, name, INFO[name]["subtitle"])
    tabs = Tabs(page, t, TABS, app.tab_memory, name)
    attach(tabs, app, name)

    viz = tabs.frames["Visualization"]
    viz.grid_columnconfigure(1, weight=1)
    viz.grid_rowconfigure(0, weight=1)

    left = tk.Frame(viz, bg=t["bg"], width=300)
    left.grid(row=0, column=0, sticky="ns", padx=(0, 16))
    left.pack_propagate(False)

    # ---- card 1: add ----
    box = card(left, t, cfg["card"])
    box.pack(fill="x", pady=(0, 14))
    row = tk.Frame(box, bg=t["panel"])
    row.pack(fill="x", padx=16, pady=(0, 16))
    value = tk.StringVar()
    field = entry(row, t, value, "Enter value")
    field.pack(side="left", fill="x", expand=True, ipady=7)
    add_btn = button(
        row, t, cfg["add"], lambda: operate(cfg["add"]), "primary",
        padx=14, pady=7
    )
    add_btn.pack(side="left", padx=(8, 0))

    # ---- card 2: other operations ----
    ops = card(left, t, "Operations")
    ops.pack(fill="x", pady=(0, 14))
    ops_row = tk.Frame(ops, bg=t["panel"])
    ops_row.pack(fill="x", padx=16, pady=(0, 16))
    actions = cfg["others"] + ["Clear"]
    for i, action in enumerate(actions):
        ops_row.grid_columnconfigure(i, weight=1, uniform="ops")
        kind = "danger" if action == "Clear" else "soft"
        command = (
            (lambda: clear_structure()) if action == "Clear"
            else (lambda a=action: operate(a))
        )
        button(ops_row, t, action, command, kind).grid(
            row=0, column=i, sticky="ew",
            padx=(0 if i == 0 else 4, 0 if i == len(actions) - 1 else 4)
        )

    # ---- card 3: history ----
    hist = card(left, t, "History")
    hist.pack(fill="x")
    hist_body = tk.Frame(hist, bg=t["panel"])
    hist_body.pack(fill="x", padx=16, pady=(0, 16))

    # ---- canvas ----
    def draw(view):
        vals = values_now(app, name)
        if not vals:
            view.empty(
                "Empty structure\n\nEnter a value and choose an operation"
            )
            return
        if name == "Binary Search Tree":
            draw_tree(
                view, t, app.models[name].root, highlight=st["highlight"]
            )
        else:
            draw_linear(view, t, name, vals)

    view = Viewport(viz, t, draw)
    view.canvas.grid(row=0, column=1, sticky="nsew")

    # ---- behaviour ----
    def refresh_history():
        for widget in hist_body.winfo_children():
            widget.destroy()
        if not st["history"]:
            muted(hist_body, t, "No operations yet").pack(fill="x")
            return
        for message in st["history"][-6:]:
            row_label(hist_body, t, message).pack(fill="x", pady=2)

    def log(message):
        st["history"].append(message)
        st["status"] = message
        refresh_history()
        view.redraw()

    def clear_structure():
        app.reset(name)
        st.update(history=[], status="Cleared", highlight=None)
        refresh_history()
        view.redraw()

    def operate(action):
        raw = value.get().strip()
        m = app.models[name]

        try:
            if action in ("Push", "Enqueue", "Insert"):
                if not raw:
                    raise ValueError("Enter an integer first.")
                v = int(raw)

                if name == "Stack":
                    m.push(v)
                elif name == "Queue":
                    m.enqueue(v)
                elif name == "Heap":
                    m.push(v)
                else:
                    m.insert(v)

                st["highlight"] = v
                value.set("")
                log(f"{action}: {v}")

            elif action in ("Pop", "Dequeue", "Extract min"):
                if name == "Stack":
                    result = m.pop()
                elif name == "Queue":
                    result = m.dequeue()
                else:
                    result = m.pop()
                st["highlight"] = None
                log(f"{action}: {result}")

            elif action == "Delete":
                if not raw:
                    raise ValueError("Enter a value to delete.")
                v = int(raw)

                if name == "Linked List":
                    result = m.delete(v)
                    log(f"Deleted {v}" if result else f"{v} not found")
                else:
                    m.delete(v)
                    log(f"Deleted {v} if present")
                st["highlight"] = None

            elif action == "Search":
                if not raw:
                    raise ValueError("Enter a value to search for.")
                v = int(raw)

                if name == "B-Tree":
                    result = m.search(v) is not None
                else:
                    result = m.search(v)

                st["highlight"] = v if result else None
                log(f"Search {v}: {result}")

        except (ValueError, IndexError) as error:
            messagebox.showerror("Operation failed", str(error))

    field.bind("<Return>", lambda e: operate(cfg["add"]))
    refresh_history()
    tabs.start()
