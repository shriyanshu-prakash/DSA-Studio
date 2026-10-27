import tkinter as tk

from ui.theme import FONT, SYMBOL


class NavItem(tk.Frame):
    """Sidebar row: fixed-width icon column so every label lines up."""

    def __init__(self, parent, glyph, text, command, compact=False):
        super().__init__(parent, cursor="hand2")
        self.active = False
        self.theme = None
        pad = 4 if compact else 6

        self.icon = tk.Label(
            self, text=glyph, width=2, font=(SYMBOL, 10), anchor="center"
        )
        self.label = tk.Label(
            self, text=text, font=(FONT, 10), anchor="w"
        )
        self.icon.pack(side="left", padx=(10, 4), pady=pad)
        self.label.pack(side="left", fill="x", expand=True, pady=pad)

        for widget in (self, self.icon, self.label):
            widget.bind("<Button-1>", lambda e: command())
            widget.bind("<Enter>", lambda e: self._hover(True))
            widget.bind("<Leave>", lambda e: self._hover(False))

    def _paint(self, bg, fg):
        self.configure(bg=bg)
        self.icon.configure(bg=bg, fg=fg)
        self.label.configure(bg=bg, fg=fg)

    def _hover(self, inside):
        if self.theme is None or self.active:
            return
        self._paint(
            self.theme["hover"] if inside else self.theme["sidebar"],
            self.theme["text"]
        )

    def style(self, theme, active):
        self.theme = theme
        self.active = active
        if active:
            self._paint(theme["accent"], "#FFFFFF")
        else:
            self._paint(theme["sidebar"], theme["text"])


class Shell:
    """Sidebar + top bar. Pages are drawn into `self.content`."""

    NAVIGATION = [("Home", "⌂"), ("Data Structures", "▤"), ("Algorithms", "⌘")]
    STRUCTURES = [
        ("Stack", "▥"), ("Queue", "⇥"), ("Linked List", "↔"),
        ("Binary Search Tree", "⑂"), ("AVL Tree", "♧"),
        ("B-Tree", "▦"), ("Heap", "⌃")
    ]
    ALGORITHMS = [("Sorting", "↕"), ("Searching", "⌕"), ("Graph Lab", "◉")]

    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.nav = {}
        self.sections = []
        self.sidebar_visible = True
        self._build()

    # ---------- construction ----------

    def _build(self):
        app = self.app
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(self.root, width=224)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.brand = tk.Label(
            self.sidebar, text="◇  DSA Studio", font=(FONT, 16, "bold"),
            anchor="w", padx=20, pady=20
        )
        self.brand.pack(fill="x")
        self.divider = tk.Frame(self.sidebar, height=1)
        self.divider.pack(fill="x", padx=12)

        self._section("Navigation", 12)
        for name, glyph in self.NAVIGATION:
            self._nav(name, glyph)

        self._section("Data Structures", 14)
        for name, glyph in self.STRUCTURES:
            self._nav(name, glyph, compact=True)

        self._section("Algorithms", 14)
        for name, glyph in self.ALGORITHMS:
            self._nav(name, glyph, compact=True)

        # Footer (user chip)
        self.footer = tk.Frame(self.sidebar)
        self.footer.pack(side="bottom", fill="x")
        self.footer_line = tk.Frame(self.footer, height=1)
        self.footer_line.pack(fill="x", padx=12)

        chip_row = tk.Frame(self.footer)
        chip_row.pack(fill="x", padx=14, pady=12)
        self.chip_row = chip_row

        self.avatar = tk.Canvas(
            chip_row, width=30, height=30, highlightthickness=0
        )
        self.avatar_oval = self.avatar.create_oval(1, 1, 29, 29, outline="")
        self.avatar.create_text(
            15, 15, text="G", fill="white", font=(FONT, 10, "bold")
        )
        self.avatar.pack(side="left")

        texts = tk.Frame(chip_row)
        texts.pack(side="left", padx=(10, 0))
        self.chip_texts = texts
        self.user_name = tk.Label(
            texts, text="Guest User", font=(FONT, 9, "bold"), anchor="w"
        )
        self.user_name.pack(fill="x")
        self.user_mode = tk.Label(
            texts, text="Local mode · no backend",
            font=(FONT, 8), anchor="w"
        )
        self.user_mode.pack(fill="x")

        # Main area
        self.main = tk.Frame(self.root)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.topbar = tk.Frame(self.main, height=54, highlightthickness=1)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        self.menu_btn = tk.Button(
            self.topbar, text="◧", command=self.toggle_sidebar,
            relief="flat", bd=0, highlightthickness=0, takefocus=0,
            font=(SYMBOL, 12), padx=8, pady=4, cursor="hand2"
        )
        self.menu_btn.pack(side="left", padx=(14, 4), pady=12)

        self.breadcrumb = tk.Label(
            self.topbar, text="Home  ›  Dashboard",
            font=(FONT, 10), anchor="w"
        )
        self.breadcrumb.pack(side="left", fill="y", padx=(8, 0))

        self.theme_btn = tk.Button(
            self.topbar, text="☾", command=app.toggle_theme,
            relief="flat", bd=0, highlightthickness=1, takefocus=0,
            font=(SYMBOL, 11), width=3, pady=3, cursor="hand2"
        )
        self.theme_btn.pack(side="right", padx=18, pady=12)

        self.content = tk.Frame(self.main)
        self.content.grid(row=1, column=0, sticky="nsew")

    def _section(self, title, top_pad):
        label = tk.Label(
            self.sidebar, text=title, font=(FONT, 8, "bold"),
            anchor="w", padx=19, pady=4
        )
        label.pack(fill="x", pady=(top_pad, 2))
        self.sections.append(label)

    def _nav(self, name, glyph, compact=False):
        item = NavItem(
            self.sidebar, glyph, name,
            lambda n=name: self.app.show_page(n), compact
        )
        item.pack(fill="x", padx=10, pady=1)
        self.nav[name] = item

    # ---------- behaviour ----------

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()
        self.sidebar_visible = not self.sidebar_visible

    def set_page(self, name):
        if name == "Home":
            text = "Home  ›  Dashboard"
        elif name in ("Data Structures", "Algorithms"):
            text = f"Home  ›  {name}"
        else:
            text = f"Home  ›  Visualizer  ›  {name}"
        self.breadcrumb.configure(text=text)

    def apply_theme(self, theme, dark, page):
        t = theme
        self.root.configure(bg=t["bg"])

        for widget in (
            self.sidebar, self.footer, self.chip_row, self.chip_texts
        ):
            widget.configure(bg=t["sidebar"])
        self.brand.configure(bg=t["sidebar"], fg=t["text"])
        self.divider.configure(bg=t["border"])
        self.footer_line.configure(bg=t["border"])

        for label in self.sections:
            label.configure(bg=t["sidebar"], fg=t["muted"])

        self.avatar.configure(bg=t["sidebar"])
        self.avatar.itemconfigure(self.avatar_oval, fill=t["accent"])
        self.user_name.configure(bg=t["sidebar"], fg=t["text"])
        self.user_mode.configure(bg=t["sidebar"], fg=t["muted"])

        for name, item in self.nav.items():
            item.style(t, name == page)

        self.main.configure(bg=t["bg"])
        self.content.configure(bg=t["bg"])
        self.topbar.configure(
            bg=t["panel"], highlightbackground=t["border"]
        )
        self.breadcrumb.configure(bg=t["panel"], fg=t["muted"])
        self.menu_btn.configure(
            bg=t["panel"], fg=t["muted"],
            activebackground=t["hover"], activeforeground=t["text"]
        )
        self.theme_btn.configure(
            bg=t["panel"], fg=t["text"], highlightbackground=t["border"],
            activebackground=t["hover"], activeforeground=t["text"],
            text="☼" if dark else "☾"
        )
