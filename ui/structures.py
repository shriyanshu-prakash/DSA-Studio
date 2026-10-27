import tkinter as tk
from tkinter import messagebox

from ui.theme import FONT
from ui.content import INFO, TABS
from ui.info_tabs import attach
from ui.treeview import draw_tree
from ui.widgets import new_page, page_header, card, muted, button, entry, row_label, Tabs, Viewport

CONFIG = {
    "Stack": {"add": "Push", "card": "Push Value", "others": ["Pop"]},
    "Queue": {"add": "Enqueue", "card": "Enqueue Value", "others": ["Dequeue"]},
    "Linked List": {"add": "Insert", "card": "Insert Node", "others": ["Delete", "Search"]},
    "Binary Search Tree": {"add": "Insert", "card": "Insert Node", "others": ["Delete", "Search"]},
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


def draw_linear(view, t, name, vals, highlight=None, visible_count=None):
    c, w, h, s = view.canvas, view.w, view.h, view.s
    vals = vals if visible_count is None else vals[:visible_count]
    if not vals:
        view.empty("Empty structure\n\nEnter a value and choose an operation")
        return

    if name == "Stack":
        boxw = min(100, max(58, (w - 90) / max(1, len(vals))))
        for i, value in enumerate(vals):
            cx, cy = w / 2, h - 62 - i * 52
            x1, y1 = view.tx(cx - boxw / 2, cy - 21)
            x2, y2 = view.tx(cx + boxw / 2, cy + 21)
            hot = value == highlight
            c.create_rectangle(x1, y1, x2, y2, fill=t["accent"] if hot else t["node"], outline=t["border"], width=1)
            c.create_text((x1+x2)/2, (y1+y2)/2, text=str(value), fill="white", font=view.font(11))
        c.create_text(*view.tx(w/2, 24), text="TOP", fill=t["accent"], font=view.font(9))
        return

    if name == "Linked List":
        # A wide virtual layout lets zoom/pan handle longer lists without squashing nodes.
        boxw, boxh, gap = 82, 46, 42
        total = len(vals) * boxw + max(0, len(vals)-1) * gap + 75
        start_x = max(30, (w-total)/2) if total < w-30 else 30
        cy = h / 2
        for i, value in enumerate(vals):
            x = start_x + i * (boxw + gap)
            x1, y1 = view.tx(x, cy-boxh/2)
            x2, y2 = view.tx(x+boxw, cy+boxh/2)
            hot = value == highlight
            c.create_rectangle(x1, y1, x2, y2, fill=t["accent"] if hot else t["node"], outline=t["border"], width=1)
            c.create_text((x1+x2)/2, (y1+y2)/2, text=str(value), fill="white", font=view.font(11))
            if i < len(vals)-1:
                ax, ay = view.tx(x+boxw+3, cy)
                bx, by = view.tx(x+boxw+gap-5, cy)
                c.create_line(ax, ay, bx, by, arrow=tk.LAST, fill=t["accent"], width=max(1, 2*s))
        # Keep NULL fully to the right of the final node and connect it
        # with an arrow. Left anchoring prevents the label overlapping the node.
        last_right = start_x + (len(vals) - 1) * (boxw + gap) + boxw
        null_left = last_right + 24
        ax, ay = view.tx(last_right + 3, cy)
        bx, by = view.tx(null_left - 5, cy)
        c.create_line(
            ax, ay, bx, by, arrow=tk.LAST,
            fill=t["accent"], width=max(1, 2 * s)
        )
        nx, ny = view.tx(null_left, cy)
        c.create_text(
            nx, ny, text="NULL", fill=t["accent"],
            font=view.font(10, "bold"), anchor="w"
        )
        return

    # Queue / heap linear representation
    boxw = min(90, max(50, (w - 60) / max(1, len(vals))))
    for i, value in enumerate(vals):
        left = 25 + i * boxw
        x1, y1 = view.tx(left, h/2-22)
        x2, y2 = view.tx(left+boxw-5, h/2+22)
        hot = value == highlight
        c.create_rectangle(x1, y1, x2, y2, fill=t["accent"] if hot else t["node"], outline=t["border"])
        c.create_text((x1+x2)/2, (y1+y2)/2, text=str(value), fill="white", font=view.font(11))


def build(app, name):
    t = app.theme
    cfg = CONFIG[name]
    st = app.state.setdefault(name, {"history": [], "status": "Ready", "highlight": None, "speed": 5, "visible_count": None, "animating": False, "animation_id": None})
    st.setdefault("speed", 5)
    st.setdefault("visible_count", None)
    st.setdefault("animating", False)
    st.setdefault("animation_id", None)

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

    box = card(left, t, cfg["card"])
    box.pack(fill="x", pady=(0, 14))
    row = tk.Frame(box, bg=t["panel"])
    row.pack(fill="x", padx=16, pady=(0, 16))
    value = tk.StringVar()
    field = entry(row, t, value, "Enter integer")
    field.pack(side="left", fill="x", expand=True, ipady=7)
    button(row, t, cfg["add"], lambda: operate(cfg["add"]), "primary", padx=14, pady=7).pack(side="left", padx=(8, 0))

    ops = card(left, t, "Operations")
    ops.pack(fill="x", pady=(0, 14))
    ops_row = tk.Frame(ops, bg=t["panel"])
    ops_row.pack(fill="x", padx=12, pady=(0, 14))
    actions = cfg["others"] + ["Clear"]
    for i, action in enumerate(actions):
        ops_row.grid_columnconfigure(i, weight=1, uniform="ops")
        command = (
            (lambda: clear_structure())
            if action == "Clear"
            else (lambda a=action: operate(a))
        )
        button(ops_row, t, action, command, "danger" if action == "Clear" else "soft", padx=6).grid(row=0, column=i, sticky="ew", padx=3)

    speed_card = card(left, t, "Animation speed")
    speed_card.pack(fill="x", pady=(0, 14))
    speed_var = tk.IntVar(value=st["speed"])
    speed_label = tk.Label(speed_card, text=f"{speed_var.get()} / 10", bg=t["panel"], fg=t["muted"], font=(FONT, 9))
    speed_label.pack(anchor="e", padx=16)
    speed = tk.Scale(speed_card, from_=1, to=10, orient="horizontal", variable=speed_var, showvalue=False, bg=t["panel"], fg=t["text"], troughcolor=t["soft"], highlightthickness=0, bd=0, command=lambda v: (st.update(speed=int(float(v))), speed_label.configure(text=f"{int(float(v))} / 10")))
    speed.pack(fill="x", padx=12, pady=(0, 10))

    hist = card(left, t, "Recent operations")
    hist.pack(fill="both", expand=True)
    hist_body = tk.Frame(hist, bg=t["panel"])
    hist_body.pack(fill="both", expand=True, padx=16, pady=(0, 14))

    def draw(view):
        vals = values_now(app, name)
        if name == "Binary Search Tree":
            if not vals:
                view.empty("Empty structure\n\nInsert a value to begin")
            else:
                draw_tree(view, t, app.models[name].root, highlight=st["highlight"])
        else:
            draw_linear(view, t, name, vals, st["highlight"], st.get("visible_count"))

    view = Viewport(viz, t, draw)
    view.canvas.grid(row=0, column=1, sticky="nsew")

    def refresh_history():
        for widget in hist_body.winfo_children(): widget.destroy()
        if not st["history"]:
            muted(hist_body, t, "Your operations will appear here.", wraplength=250).pack(fill="x")
            return
        for message in st["history"][-5:]:
            row_label(hist_body, t, message).pack(fill="x", pady=2)

    def cancel_animation():
        job = st.get("animation_id")
        if job:
            try: app.root.after_cancel(job)
            except tk.TclError: pass
        st["animation_id"] = None
        st["animating"] = False
        st["visible_count"] = None

    def log(message):
        st["history"].append(message)
        st["status"] = message
        refresh_history()
        view.redraw()

    def animate_search(v):
        vals = values_now(app, name)
        if name != "Linked List":
            result = app.models[name].search(v) if name != "B-Tree" else app.models[name].search(v) is not None
            st["highlight"] = v if result else None
            log(f"Search {v}: {'found' if result else 'not found'}")
            return
        cancel_animation()
        st["animating"] = True
        index = 0
        delay = max(35, 550 - st["speed"] * 48)
        def tick():
            nonlocal index
            if not st["animating"]: return
            if index >= len(vals):
                st["highlight"] = None
                st["animating"] = False
                st["animation_id"] = None
                log(f"Search {v}: not found")
                return
            current = vals[index]
            st["highlight"] = current
            view.redraw()
            if current == v:
                st["animating"] = False
                st["animation_id"] = None
                st["history"].append(f"Search {v}: found at index {index}")
                refresh_history()
                return
            index += 1
            st["animation_id"] = app.root.after(delay, tick)
        tick()

    def clear_structure():
        cancel_animation()
        app.reset(name)
        st.update(history=[], status="Cleared", highlight=None, visible_count=None)
        refresh_history(); view.redraw()

    def operate(action):
        if st["animating"]:
            cancel_animation()
        raw = value.get().strip()
        m = app.models[name]
        try:
            if action in ("Push", "Enqueue", "Insert"):
                if not raw: raise ValueError("Enter an integer first.")
                v = int(raw)
                before = len(values_now(app, name))
                if name == "Stack": m.push(v)
                elif name == "Queue": m.enqueue(v)
                elif name == "Heap": m.push(v)
                elif name == "Linked List": m.insert(v, position=len(m.values()))  # append at tail
                else: m.insert(v)
                st["highlight"] = v
                value.set("")
                vals = values_now(app, name)
                if name == "Linked List":
                    st["visible_count"] = 0
                    delay = max(25, 420 - st["speed"] * 36)
                    def reveal(count=1):
                        if count > len(vals):
                            st["visible_count"] = None
                            st["animation_id"] = None
                            st["animating"] = False
                            view.redraw(); return
                        st["visible_count"] = count
                        view.redraw()
                        st["animation_id"] = app.root.after(delay, lambda: reveal(count+1))
                    st["animating"] = True
                    reveal()
                st["history"].append(f"{action}: {v}")
                refresh_history()
                if name != "Linked List": view.redraw()
            elif action in ("Pop", "Dequeue", "Extract min"):
                result = m.pop() if action in ("Pop", "Extract min") else m.dequeue()
                st["highlight"] = None
                log(f"{action}: {result}")
            elif action == "Delete":
                if not raw: raise ValueError("Enter a value to delete.")
                v = int(raw)
                if name == "Linked List":
                    vals = values_now(app, name)
                    if v not in vals: log(f"{v} not found"); return
                    st["highlight"] = v
                    view.redraw()
                    delay = max(35, 550 - st["speed"] * 48)
                    def finish_delete():
                        result = m.delete(v)
                        st["highlight"] = None
                        st["animating"] = False
                        st["animation_id"] = None
                        log(f"Deleted {v}" if result else f"{v} not found")
                    st["animation_id"] = app.root.after(delay, finish_delete)
                    st["animating"] = True
                    return
                if name == "Binary Search Tree": m.delete(v); log(f"Deleted {v} if present")
                else:
                    result = m.delete(v)
                    log(f"Deleted {v}" if result else f"{v} not found")
                st["highlight"] = None
            elif action == "Search":
                if not raw: raise ValueError("Enter a value to search for.")
                animate_search(int(raw))
        except (ValueError, IndexError) as error:
            messagebox.showerror("Operation failed", str(error))

    field.bind("<Return>", lambda e: operate(cfg["add"]))
    refresh_history()
    tabs.start()
