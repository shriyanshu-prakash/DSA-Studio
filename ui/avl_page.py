import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.treeview import draw_tree
from ui.widgets import (
    new_page, page_header, card, muted, button, entry, row_label, Tabs, Viewport
)

NAME = "AVL Tree"
ORDERS = ("In-order", "Pre-order", "Post-order")


def _walk(node, order, result):
    if node is None:
        return
    if order == "Pre-order":
        result.append(node.value)
    _walk(node.left, order, result)
    if order == "In-order":
        result.append(node.value)
    _walk(node.right, order, result)
    if order == "Post-order":
        result.append(node.value)


def _search_path(root, value):
    """Return the nodes inspected when searching for an insertion position."""
    path = []
    node = root
    while node is not None:
        path.append(node.value)
        if value == node.value:
            break
        node = node.left if value < node.value else node.right
    return path


def build(app):
    t = app.theme
    st = app.state.setdefault(NAME, {})
    st.setdefault("history", [])
    st.setdefault("highlight", None)
    st.setdefault("speed", 5)
    st.setdefault("traversal", [])
    st.setdefault("traversal_index", 0)
    st.setdefault("animation_id", None)
    st.setdefault("animating", False)
    st.setdefault("animation_token", 0)

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

    insert_card = card(left, t, "Insert Node")
    insert_card.pack(fill="x", pady=(0, 14))
    row = tk.Frame(insert_card, bg=t["panel"])
    row.pack(fill="x", padx=16, pady=(0, 16))
    value = tk.StringVar()
    field = entry(row, t, value, "Enter integer")
    field.pack(side="left", fill="x", expand=True, ipady=7)

    def cancel_animation():
        st["animation_token"] += 1
        job = st.get("animation_id")
        if job:
            try:
                app.root.after_cancel(job)
            except tk.TclError:
                pass
        st["animation_id"] = None
        st["animating"] = False

    def draw(view):
        tree = app.models[NAME]
        if tree.root is None:
            view.empty("Empty AVL tree\n\nInsert values to build a self-balancing tree")
        else:
            draw_tree(
                view, t, tree.root,
                highlight=st.get("highlight"),
                balance=tree.balance,
            )

    view = Viewport(viz, t, draw)
    view.canvas.grid(row=0, column=1, sticky="nsew")

    # ---- history ----
    history = card(left, t, "Operation / rotation history")
    history.pack(fill="both", expand=True, pady=(0, 0))
    history_body = tk.Frame(history, bg=t["panel"])
    history_body.pack(fill="both", expand=True, padx=16, pady=(0, 14))

    def history_refresh():
        for widget in history_body.winfo_children():
            widget.destroy()
        if not st["history"]:
            muted(
                history_body, t,
                "Insertions, traversals and rotations will appear here.",
                wraplength=250,
            ).pack(fill="x")
        else:
            for message in st["history"][-7:]:
                row_label(history_body, t, message).pack(fill="x", pady=2)

    def add_history(message):
        st["history"].append(message)
        history_refresh()

    # ---- actions ----
    actions = card(left, t, "Operations")
    actions.pack(fill="x", pady=(0, 14))
    action_row = tk.Frame(actions, bg=t["panel"])
    action_row.pack(fill="x", padx=12, pady=(0, 14))

    # ---- traversal ----
    traversal_card = card(left, t, "Traversal")
    traversal_card.pack(fill="x", pady=(0, 14))
    order = tk.StringVar(value="In-order")
    choices = tk.Frame(traversal_card, bg=t["panel"])
    choices.pack(fill="x", padx=12, pady=(0, 8))
    traversal_result = tk.Label(
        traversal_card,
        text="Choose a traversal to see its order.",
        bg=t["panel"], fg=t["muted"], font=(FONT, 9),
        justify="left", anchor="w", wraplength=250,
    )
    traversal_result.pack(fill="x", padx=16, pady=(0, 12))

    # ---- speed ----
    speed_card = card(left, t, "Animation speed")
    speed_card.pack(fill="x", pady=(0, 14))
    speed_label = tk.Label(
        speed_card, text=f"{st['speed']} / 10", bg=t["panel"],
        fg=t["muted"], font=(FONT, 9),
    )
    speed_label.pack(anchor="e", padx=16)

    def speed_changed(raw):
        speed_value = int(float(raw))
        st["speed"] = speed_value
        speed_label.configure(text=f"{speed_value} / 10")

    speed = tk.Scale(
        speed_card, from_=1, to=10, orient="horizontal", showvalue=False,
        bg=t["panel"], fg=t["text"], troughcolor=t["soft"],
        highlightthickness=0, bd=0, command=speed_changed,
    )
    speed.set(st["speed"])
    speed.pack(fill="x", padx=12, pady=(0, 10))

    def delay_ms():
        # 1 = slow, 10 = fast; every frame is scheduled with after().
        return max(65, 650 - st["speed"] * 55)

    def clear_tree():
        cancel_animation()
        app.reset(NAME)
        st.update(history=[], highlight=None, traversal=[], traversal_index=0)
        traversal_result.configure(text="Choose a traversal to see its order.")
        history_refresh()
        view.redraw()

    def reset_view():
        st["highlight"] = None
        view.fit()
        view.redraw()

    button(action_row, t, "Clear tree", clear_tree, "danger").pack(
        side="left", fill="x", expand=True, padx=(0, 4)
    )
    button(action_row, t, "Reset view", reset_view, "soft").pack(
        side="left", fill="x", expand=True, padx=(4, 0)
    )

    def insert():
        raw = value.get().strip()
        if not raw:
            messagebox.showerror("Invalid input", "Enter an integer first.")
            return
        try:
            number = int(raw)
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a valid integer.")
            return

        cancel_animation()
        tree = app.models[NAME]
        path = _search_path(tree.root, number)
        # Detect duplicates before starting the animation.
        node = tree.root
        while node is not None:
            if number == node.value:
                messagebox.showerror("Insert failed", "That value is already in the tree.")
                return
            node = node.left if number < node.value else node.right

        old_rotation_count = len(tree.rotations)
        value.set("")
        st["animating"] = True
        token = st["animation_token"]
        add_history(f"Inserting {number} · tracing search path")
        traversal_result.configure(text=f"Insert {number}\nFinding its position…")

        def finish_insert():
            if token != st["animation_token"]:
                return
            try:
                tree.insert(number)
            except ValueError as error:
                st["animating"] = False
                messagebox.showerror("Insert failed", str(error))
                return

            rotations = tree.rotations[old_rotation_count:]
            messages = [f"Inserted {number}"]
            messages.extend(f"{direction} rotation at {pivot}" for direction, pivot in rotations)
            for message in messages:
                st["history"].append(message)
            history_refresh()

            # Animate through the rotation pivots, then settle on the inserted node.
            focus_values = [pivot for _direction, pivot in rotations] + [number]
            if not focus_values:
                focus_values = [number]

            def focus(index=0):
                if token != st["animation_token"]:
                    return
                if index >= len(focus_values):
                    st["highlight"] = None
                    st["animating"] = False
                    st["animation_id"] = None
                    traversal_result.configure(text=f"Inserted {number} successfully.")
                    view.redraw()
                    return
                st["highlight"] = focus_values[index]
                traversal_result.configure(
                    text=(f"Balancing tree…\n{rotations[index][0]} rotation at {rotations[index][1]}"
                          if index < len(rotations) else f"Inserted node: {number}")
                )
                view.redraw()
                st["animation_id"] = app.root.after(delay_ms(), lambda: focus(index + 1))

            view.redraw()
            focus()

        def trace(index=0):
            if token != st["animation_token"]:
                return
            if index >= len(path):
                st["animation_id"] = app.root.after(delay_ms(), finish_insert)
                return
            st["highlight"] = path[index]
            traversal_result.configure(
                text=f"Insert {number}\nComparing with {path[index]} ({index + 1}/{len(path)})"
            )
            view.redraw()
            st["animation_id"] = app.root.after(delay_ms(), lambda: trace(index + 1))

        trace()

    button(row, t, "Insert", insert, "primary", padx=14, pady=7).pack(
        side="left", padx=(8, 0)
    )
    field.bind("<Return>", lambda _event: insert())

    def choose_order(selected):
        cancel_animation()
        order.set(selected)
        result = []
        _walk(app.models[NAME].root, selected, result)
        st["traversal"] = result
        st["traversal_index"] = 0
        if not result:
            st["highlight"] = None
            traversal_result.configure(text="The tree is empty.")
            view.redraw()
            return

        add_history(f"Started {selected.lower()} traversal")
        token = st["animation_token"]
        st["animating"] = True
        delay = delay_ms()

        def tick(index=0):
            if token != st["animation_token"]:
                return
            if index >= len(result):
                st["highlight"] = None
                st["animating"] = False
                st["animation_id"] = None
                traversal_result.configure(
                    text=f"{selected}:\n" + " → ".join(map(str, result))
                )
                view.redraw()
                add_history(f"Completed {selected.lower()} traversal")
                return
            st["highlight"] = result[index]
            st["traversal_index"] = index
            traversal_result.configure(
                text=f"{selected}\nVisiting {index + 1}/{len(result)}: {result[index]}"
            )
            view.redraw()
            st["animation_id"] = app.root.after(delay, lambda: tick(index + 1))

        tick()

    for label in ORDERS:
        button(
            choices, t, label,
            lambda selected=label: choose_order(selected),
            "soft", padx=5, pady=6,
        ).pack(fill="x", pady=2)

    history_refresh()
    tabs.start()
