import tkinter as tk

from ui.theme import FONT


# ---------- helpers ----------

def mix(fg, bg, amount):
    """Blend fg over bg. amount=0 -> bg, amount=1 -> fg."""
    def rgb(c):
        c = c.lstrip("#")
        return [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    f, b = rgb(fg), rgb(bg)
    return "#%02x%02x%02x" % tuple(
        int(b[i] + (f[i] - b[i]) * amount) for i in range(3)
    )


def new_page(app):
    page = tk.Frame(app.content, bg=app.theme["bg"])
    page.pack(fill="both", expand=True, padx=28, pady=(22, 22))
    return page


def page_header(parent, t, title, subtitle):
    frame = tk.Frame(parent, bg=t["bg"])
    frame.pack(fill="x", pady=(0, 16))
    tk.Label(
        frame, text=title, bg=t["bg"], fg=t["text"],
        font=(FONT, 22, "bold"), anchor="w"
    ).pack(fill="x")
    tk.Label(
        frame, text=subtitle, bg=t["bg"], fg=t["muted"],
        font=(FONT, 10), anchor="w", justify="left", wraplength=1000
    ).pack(fill="x", pady=(4, 0))


def card(parent, t, title=None):
    frame = tk.Frame(
        parent, bg=t["panel"],
        highlightbackground=t["border"], highlightthickness=1
    )
    if title:
        tk.Label(
            frame, text=title, bg=t["panel"], fg=t["text"],
            font=(FONT, 11, "bold"), anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 10))
    return frame


def muted(parent, t, text, bg=None, **kw):
    return tk.Label(
        parent, text=text, bg=bg or t["panel"], fg=t["muted"],
        font=(FONT, 9), anchor="w", justify="left", **kw
    )


def button(parent, t, text, command, kind="soft", **kw):
    styles = {
        "primary": (t["button"], t["button_text"], t["accent"], "bold"),
        "soft": (t["soft"], t["muted"], t["hover"], "normal"),
        "danger": (t["danger"], "#FFFFFF", t["danger_hover"], "bold"),
    }
    bg, fg, active, weight = styles[kind]
    options = dict(
        text=text, command=command, bg=bg, fg=fg,
        activebackground=active,
        activeforeground="#FFFFFF" if kind != "soft" else t["text"],
        relief="flat", bd=0, highlightthickness=0, takefocus=0,
        font=(FONT, 9, weight), cursor="hand2", padx=12, pady=7
    )
    options.update(kw)
    return tk.Button(parent, **options)


def entry(parent, t, var, placeholder="", **kw):
    options = dict(
        textvariable=var, font=(FONT, 10), relief="flat", bd=0,
        bg=t["entry_bg"], fg=t["text"], insertbackground=t["text"],
        highlightthickness=1, highlightbackground=t["border"],
        highlightcolor=t["accent"]
    )
    options.update(kw)
    widget = tk.Entry(parent, **options)

    if placeholder:
        hint = tk.Label(
            widget, text=placeholder, bg=t["entry_bg"], fg=t["muted"],
            font=(FONT, 10), cursor="xterm"
        )
        hint.bind("<Button-1>", lambda e: widget.focus_set())

        def refresh(*_):
            try:
                if var.get():
                    hint.place_forget()
                else:
                    hint.place(x=8, rely=0.5, anchor="w")
            except tk.TclError:
                pass

        var.trace_add("write", refresh)
        refresh()

    return widget


def option_menu(parent, t, var, options):
    menu = tk.OptionMenu(parent, var, *options)
    menu.configure(
        bg=t["soft"], fg=t["text"], activebackground=t["hover"],
        activeforeground=t["text"], relief="flat", bd=0,
        highlightthickness=0, font=(FONT, 10), padx=10, pady=6,
        cursor="hand2"
    )
    menu["menu"].configure(
        bg=t["panel"], fg=t["text"], activebackground=t["accent"],
        activeforeground="#FFFFFF", relief="flat", bd=0, font=(FONT, 10)
    )
    return menu


def chip(parent, t, text):
    return tk.Label(
        parent, text=text, bg=t["chip"], fg=t["chip_text"],
        font=(FONT, 9, "bold"), padx=9, pady=4
    )


def row_label(parent, t, text, warn=False):
    if warn:
        bg, fg, border = t["warn_bg"], t["warn_fg"], t["warn_border"]
    else:
        bg, fg, border = t["soft"], t["text"], t["soft"]
    return tk.Label(
        parent, text=text, bg=bg, fg=fg, font=(FONT, 9), anchor="w",
        padx=10, pady=6, highlightthickness=1, highlightbackground=border
    )


# ---------- tabs ----------

class Tabs:
    """Segmented tab bar (Visualization / Analysis / Explanation)."""

    def __init__(self, parent, t, names, memory, key):
        self.t = t
        self.memory = memory
        self.key = key
        self.names = names
        self.on_show = {}
        self.frames = {}
        self.labels = {}

        self.bar = tk.Frame(parent, bg=t["tabbar"], padx=4, pady=4)
        self.bar.pack(fill="x")
        self.body = tk.Frame(parent, bg=t["bg"])
        self.body.pack(fill="both", expand=True, pady=(14, 0))

        for i, name in enumerate(names):
            self.bar.grid_columnconfigure(i, weight=1, uniform="tab")
            label = tk.Label(
                self.bar, text=name, cursor="hand2", pady=6,
                font=(FONT, 10)
            )
            label.grid(row=0, column=i, sticky="ew", padx=1)
            label.bind("<Button-1>", lambda e, n=name: self.select(n))
            self.labels[name] = label
            self.frames[name] = tk.Frame(self.body, bg=t["bg"])

    def start(self):
        self.select(self.memory.get(self.key, self.names[0]))

    def select(self, name):
        t = self.t
        self.memory[self.key] = name

        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

        callback = self.on_show.get(name)
        if callback:
            callback(self.frames[name])

        for n, label in self.labels.items():
            active = n == name
            label.configure(
                bg=t["tab_active"] if active else t["tabbar"],
                fg=t["text"] if active else t["muted"],
                font=(FONT, 10, "bold" if active else "normal")
            )


# ---------- wrapping chip layout ----------

class Flow(tk.Frame):
    def __init__(self, parent, bg, gap=6):
        super().__init__(parent, bg=bg, height=1)
        self.gap = gap
        self.items = []
        self.bind("<Configure>", lambda e: self.layout())

    def add(self, widget):
        self.items.append(widget)
        self.layout()

    def layout(self):
        width = self.winfo_width()
        if width < 40:
            width = 250
        x = y = row_height = 0

        for widget in self.items:
            widget.update_idletasks()
            w, h = widget.winfo_reqwidth(), widget.winfo_reqheight()
            if x + w > width and x > 0:
                x = 0
                y += row_height + self.gap
                row_height = 0
            widget.place(x=x, y=y)
            x += w + self.gap
            row_height = max(row_height, h)

        wanted = max(1, y + row_height)
        if int(self.cget("height")) != wanted:
            self.configure(height=wanted)


# ---------- zoom / pan canvas ----------

class Viewport:
    """Dotted canvas with zoom, pan and the small control pad."""

    def __init__(self, parent, t, draw, controls=True):
        self.t = t
        self.draw_cb = draw
        self.s = 1.0
        self.px = 0.0
        self.py = 0.0
        self.locked = False
        self._last = (0, 0)

        self.canvas = tk.Canvas(
            parent, bg=t["canvas"], bd=0,
            highlightthickness=1, highlightbackground=t["border"]
        )
        self.canvas.bind("<Configure>", self._resized)

        if controls:
            self.canvas.bind("<ButtonPress-1>", self._press)
            self.canvas.bind("<B1-Motion>", self._drag)
            self.canvas.bind("<MouseWheel>", self._wheel)
            self._build_controls()

    # geometry
    @property
    def w(self):
        return max(self.canvas.winfo_width(), 400)

    @property
    def h(self):
        return max(self.canvas.winfo_height(), 300)

    def tx(self, x, y):
        cx, cy = self.w / 2, self.h / 2
        return (cx + (x - cx) * self.s + self.px,
                cy + (y - cy) * self.s + self.py)

    def font(self, size, weight="bold"):
        return (FONT, max(6, int(round(size * self.s))), weight)

    # drawing
    def _resized(self, event=None):
        c = self.canvas
        c.delete("grid")
        w, h = c.winfo_width(), c.winfo_height()
        for x in range(12, w, 22):
            for y in range(12, h, 22):
                c.create_oval(
                    x, y, x + 2, y + 2,
                    fill=self.t["dot"], outline="", tags="grid"
                )
        c.tag_lower("grid")
        self.redraw()

    def redraw(self):
        self.canvas.delete("!grid")
        self.draw_cb(self)

    def empty(self, text):
        self.canvas.create_text(
            self.w / 2, self.h / 2, text=text, fill=self.t["muted"],
            font=(FONT, 12), justify="center"
        )

    # interaction
    def _press(self, event):
        self._last = (event.x, event.y)

    def _drag(self, event):
        if self.locked:
            return
        self.px += event.x - self._last[0]
        self.py += event.y - self._last[1]
        self._last = (event.x, event.y)
        self.redraw()

    def _wheel(self, event):
        if not self.locked:
            self.zoom(1.1 if event.delta > 0 else 1 / 1.1)

    def zoom(self, factor):
        self.s = max(0.4, min(2.5, self.s * factor))
        self.redraw()

    def fit(self):
        self.s, self.px, self.py = 1.0, 0.0, 0.0
        self.redraw()

    def _toggle_lock(self):
        self.locked = not self.locked
        self.lock_btn.configure(text="🔒" if self.locked else "🔓")

    def _build_controls(self):
        t = self.t
        pad = tk.Frame(
            self.canvas, bg=t["panel"],
            highlightbackground=t["border"], highlightthickness=1
        )
        pad.place(relx=1.0, rely=1.0, x=-14, y=-14, anchor="se")

        def make(text, command):
            b = tk.Button(
                pad, text=text, command=command, bg=t["panel"],
                fg=t["text"], activebackground=t["hover"],
                activeforeground=t["text"], relief="flat", bd=0,
                highlightthickness=0, takefocus=0, width=3, pady=3,
                font=(FONT, 10), cursor="hand2"
            )
            b.pack(side="left")
            return b

        make("+", lambda: self.zoom(1.2))
        make("−", lambda: self.zoom(1 / 1.2))
        make("⤢", self.fit)
        self.lock_btn = make("🔓", self._toggle_lock)
