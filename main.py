import tkinter as tk
from tkinter import messagebox
import math

from algorithms.linked_list import LinkedList
from algorithms.linear_structures import Stack, Queue, MinHeap
from algorithms.bst import BinarySearchTree
from algorithms.btree import BTree
from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort
)
from algorithms.searching import linear_search, binary_search
from algorithms.graphs import Graph

THEMES = {
    "light": {
        "bg": "#F6F6F5", "panel": "#FFFFFF", "sidebar": "#FAFAF9",
        "text": "#202124", "muted": "#777777", "border": "#E5E5E5",
        "node": "#45566B", "accent": "#A34FF0", "button": "#27272A",
        "button_text": "#FFFFFF", "canvas": "#FFFFFF", "hover": "#F0E7FC",
        "soft": "#F7F4FA", "danger": "#EF4444"
    },
    "dark": {
        "bg": "#17191D", "panel": "#22252B", "sidebar": "#1C1E23",
        "text": "#F4F4F5", "muted": "#A1A1AA", "border": "#34373E",
        "node": "#45566B", "accent": "#B66BFF", "button": "#A34FF0",
        "button_text": "#FFFFFF", "canvas": "#202329", "hover": "#30263D",
        "soft": "#29232F", "danger": "#EF4444"
    }
}


# ==================== AVL TREE ====================

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        middle = x.right
        x.right = y
        y.left = middle

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        middle = y.left
        y.left = x
        x.right = middle

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert_node(self, node, value):
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self.insert_node(node.left, value)
        elif value > node.value:
            node.right = self.insert_node(node.right, value)
        else:
            raise ValueError("That value is already in the tree.")

        node.height = 1 + max(
            self.height(node.left), self.height(node.right)
        )
        balance = self.balance(node)

        if balance > 1 and value < node.left.value:
            return self.rotate_right(node)

        if balance < -1 and value > node.right.value:
            return self.rotate_left(node)

        if balance > 1 and value > node.left.value:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, value):
        self.root = self.insert_node(self.root, value)

    def traversal(self, order):
        result = []

        def visit(node):
            if not node:
                return

            if order == "Pre-order":
                result.append(node.value)

            visit(node.left)

            if order == "In-order":
                result.append(node.value)

            visit(node.right)

            if order == "Post-order":
                result.append(node.value)

        visit(self.root)
        return result


# ==================== MAIN APPLICATION ====================

class DSAStudio:
    def __init__(self, root):
        self.root = root
        self.dark = False
        self.theme = THEMES["light"]
        self.page = "Home"
        self.last_highlight = None

        # Data structures
        self.avl = AVLTree()
        self.stack = Stack()
        self.queue = Queue()
        self.linked = LinkedList()
        self.bst = BinarySearchTree()
        self.btree = BTree()
        self.heap = MinHeap()
        self.graph = Graph()

        # Sorting state
        self.sort_steps = []
        self.sort_step = 0

        root.title("DSA Studio | Algorithm Visualizer")
        root.geometry("1360x820")
        root.minsize(1050, 680)

        self._build_shell()
        self.apply_theme()
        self.show_page("Home")

    # ==================== UI SHELL ====================

    def _build_shell(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(self.root, width=218)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.brand = tk.Label(
            self.sidebar,
            text="◇  DSA Studio",
            font=("Segoe UI", 16, "bold"),
            anchor="w", padx=18, pady=22
        )
        self.brand.pack(fill="x")

        tk.Label(
            self.sidebar, text="NAVIGATION",
            font=("Segoe UI", 8, "bold"),
            anchor="w", padx=19, pady=8
        ).pack(fill="x", pady=(12, 3))

        self.nav_buttons = {}

        for name, glyph in [
            ("Home", "⌂"),
            ("Data Structures", "▤"),
            ("Algorithms", "⌘")
        ]:
            self.add_nav(name, glyph)

        tk.Label(
            self.sidebar, text="DATA STRUCTURES",
            font=("Segoe UI", 8, "bold"),
            anchor="w", padx=19, pady=8
        ).pack(fill="x", pady=(20, 3))

        for name, glyph in [
            ("Stack", "▥"),
            ("Queue", "⇥"),
            ("Linked List", "↔"),
            ("Binary Search Tree", "⑂"),
            ("AVL Tree", "♧"),
            ("B-Tree", "▦"),
            ("Heap", "⌃"),
            ("Sorting", "↕"),
            ("Searching", "⌕"),
            ("Graph Lab", "◉")
        ]:
            self.add_nav(name, glyph, True)

        tk.Label(
            self.sidebar, text="●  LOCAL MODE  ·  NO BACKEND",
            font=("Segoe UI", 8), anchor="w",
            padx=15, pady=14
        ).pack(side="bottom", fill="x")

        self.main = tk.Frame(self.root)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.topbar = tk.Frame(
            self.main, height=54, highlightthickness=1
        )
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        self.breadcrumb = tk.Label(
            self.topbar, text="Home  ›  Dashboard",
            font=("Segoe UI", 10), anchor="w"
        )
        self.breadcrumb.pack(side="left", fill="y", padx=24)

        self.theme_btn = tk.Button(
            self.topbar, text="☾  Dark mode",
            command=self.toggle_theme, relief="flat",
            bd=0, padx=14, pady=7, cursor="hand2"
        )
        self.theme_btn.pack(side="right", padx=18, pady=8)

        self.content = tk.Frame(self.main)
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

    def add_nav(self, name, glyph, compact=False):
        button = tk.Button(
            self.sidebar,
            text=f"{glyph}   {name}",
            anchor="w", relief="flat", bd=0,
            font=("Segoe UI", 10), padx=15,
            pady=7 if compact else 10,
            cursor="hand2",
            command=lambda n=name: self.show_page(n)
        )
        button.pack(fill="x", padx=9, pady=1)
        self.nav_buttons[name] = button

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["bg"])

        for widget, color in [
            (self.sidebar, t["sidebar"]),
            (self.main, t["bg"]),
            (self.topbar, t["panel"]),
            (self.content, t["bg"])
        ]:
            widget.configure(bg=color)

        self.brand.configure(
            bg=t["sidebar"], fg=t["text"]
        )
        self.breadcrumb.configure(
            bg=t["panel"], fg=t["muted"]
        )
        self.theme_btn.configure(
            bg=t["panel"], fg=t["text"],
            activebackground=t["hover"],
            activeforeground=t["text"],
            text="☼  Light mode" if self.dark else "☾  Dark mode"
        )
        self.topbar.configure(highlightbackground=t["border"])

        for name, button in self.nav_buttons.items():
            active = name == self.page
            button.configure(
                bg=t["accent"] if active else t["sidebar"],
                fg="#FFFFFF" if active else t["text"],
                activebackground=t["hover"],
                activeforeground=t["text"]
            )

    def toggle_theme(self):
        self.dark = not self.dark
        self.theme = THEMES["dark" if self.dark else "light"]
        self.show_page(self.page)

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle):
        frame = tk.Frame(self.content, bg=self.theme["bg"])
        frame.grid(
            row=0, column=0, sticky="ew",
            padx=26, pady=(22, 16)
        )

        tk.Label(
            frame, text=title, bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 24, "bold"), anchor="w"
        ).pack(fill="x")

        tk.Label(
            frame, text=subtitle, bg=self.theme["bg"],
            fg=self.theme["muted"],
            font=("Segoe UI", 10), anchor="w",
            wraplength=1000, justify="left"
        ).pack(fill="x", pady=(4, 0))

    def card(self, parent):
        return tk.Frame(
            parent, bg=self.theme["panel"],
            highlightbackground=self.theme["border"],
            highlightthickness=1
        )

    # ==================== NAVIGATION ====================

    def show_page(self, name):
        self.page = name
        self.clear()

        self.breadcrumb.configure(
            text=f"Home  ›  {name if name != 'Home' else 'Dashboard'}"
        )

        self.apply_theme()

        if name == "Home":
            self.dashboard()
        elif name == "AVL Tree":
            self.avl_page()
        elif name in (
            "Stack", "Queue", "Linked List",
            "Binary Search Tree", "B-Tree", "Heap"
        ):
            self.structure_page(name)
        elif name == "Sorting":
            self.sorting_page()
        elif name == "Searching":
            self.searching_page()
        elif name == "Graph Lab":
            self.graph_page()
        elif name in ("Data Structures", "Algorithms"):
            self.category_page(name)

    # ==================== DASHBOARD ====================

    def dashboard(self):
        self.heading(
            "Welcome to DSA Studio",
            "Explore data structures and watch algorithms come to life."
        )

        grid = tk.Frame(self.content, bg=self.theme["bg"])
        grid.grid(
            row=1, column=0, sticky="nsew",
            padx=26, pady=(0, 24)
        )
        grid.grid_columnconfigure((0, 1), weight=1, uniform="cards")
        grid.grid_rowconfigure((0, 1), weight=1, uniform="rows")

        cards = [
            ("01", "Linear Structures",
             "Stack, Queue and Linked List", "Data Structures"),
            ("02", "Tree Visualizer",
             "BST, AVL Tree and B-Tree", "AVL Tree"),
            ("03", "Algorithm Lab",
             "Sorting and searching", "Algorithms"),
            ("04", "Graph Lab",
             "BFS, DFS and shortest paths", "Graph Lab")
        ]

        for i, (num, title, desc, destination) in enumerate(cards):
            r, c = divmod(i, 2)
            card = self.card(grid)
            card.grid(
                row=r, column=c, sticky="nsew",
                padx=9, pady=9
            )

            tk.Label(
                card, text=num, bg=self.theme["panel"],
                fg=self.theme["accent"],
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", padx=20, pady=(18, 7))

            tk.Label(
                card, text=title, bg=self.theme["panel"],
                fg=self.theme["text"],
                font=("Segoe UI", 15, "bold")
            ).pack(anchor="w", padx=20, pady=3)

            tk.Label(
                card, text=desc, bg=self.theme["panel"],
                fg=self.theme["muted"], font=("Segoe UI", 10)
            ).pack(anchor="w", padx=20, pady=3)

            tk.Button(
                card, text="Open visualizer  →",
                command=lambda d=destination: self.show_page(d),
                bg=self.theme["button"],
                fg=self.theme["button_text"],
                relief="flat", bd=0, padx=12, pady=8,
                cursor="hand2"
            ).pack(anchor="w", padx=20, pady=(12, 18))

    def category_page(self, category):
        self.heading(category, "Choose a module to explore.")

        names = (
            ["Stack", "Queue", "Linked List", "Binary Search Tree",
             "AVL Tree", "B-Tree", "Heap"]
            if category == "Data Structures"
            else ["Sorting", "Searching", "Graph Lab"]
        )

        panel = self.card(self.content)
        panel.grid(row=1, column=0, sticky="new", padx=26)

        for name in names:
            tk.Button(
                panel, text=f"◇   {name}     →",
                anchor="w",
                command=lambda n=name: self.show_page(n),
                bg=self.theme["panel"],
                fg=self.theme["text"],
                activebackground=self.theme["hover"],
                relief="flat", bd=0, padx=20, pady=12
            ).pack(fill="x")

    # ==================== DATA STRUCTURE VISUALIZERS ====================

    def structure_page(self, name):
        self.heading(
            name,
            f"Perform operations and visualize your {name.lower()}."
        )

        body = tk.Frame(self.content, bg=self.theme["bg"])
        body.grid(
            row=1, column=0, sticky="nsew",
            padx=26, pady=(0, 22)
        )
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = self.card(body)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 14))
        left.configure(width=270)
        left.grid_propagate(False)

        tk.Label(
            left, text="Operations", bg=self.theme["panel"],
            fg=self.theme["text"], font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        value = tk.StringVar()
        entry = tk.Entry(left, textvariable=value, font=("Segoe UI", 11))
        entry.pack(fill="x", padx=14, pady=(0, 8), ipady=7)

        status = tk.Label(
            left, text="Ready", bg=self.theme["panel"],
            fg=self.theme["muted"], wraplength=240,
            justify="left", anchor="w"
        )
        status.pack(fill="x", padx=14, pady=8)

        history = tk.Listbox(
            left, height=7, font=("Consolas", 9),
            bg=self.theme["panel"], fg=self.theme["text"],
            relief="flat", bd=0, highlightthickness=0
        )
        history.pack(fill="both", expand=True, padx=12, pady=10)

        canvas = tk.Canvas(
            body, bg=self.theme["canvas"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        canvas.grid(row=0, column=1, sticky="nsew")

        def values_now():
            if name == "Stack":
                return self.stack.values()
            if name == "Queue":
                return self.queue.values()
            if name == "Linked List":
                return self.linked.values()
            if name == "Binary Search Tree":
                return self.bst.inorder()
            if name == "B-Tree":
                return self.btree.inorder()
            return self.heap.items.copy()

        def draw():
            canvas.delete("all")
            w = max(canvas.winfo_width(), 400)
            h = max(canvas.winfo_height(), 300)
            t = self.theme

            for x in range(12, w, 22):
                for y in range(12, h, 22):
                    canvas.create_oval(
                        x, y, x+2, y+2,
                        fill=t["border"], outline=""
                    )

            vals = values_now()

            if not vals:
                canvas.create_text(
                    w/2, h/2,
                    text="Empty structure\n\nEnter a value and choose an operation",
                    fill=t["muted"], font=("Segoe UI", 12),
                    justify="center"
                )
                return

            if name == "Binary Search Tree":
                nodes = []
                coords = {}

                def collect(node, depth=0):
                    if node:
                        collect(node.left, depth+1)
                        nodes.append((node, depth))
                        collect(node.right, depth+1)

                collect(self.bst.root)
                index = [0]

                def position(node, depth=0):
                    if not node:
                        return
                    position(node.left, depth+1)
                    coords[node.value] = (
                        40 + (w-80)*(index[0]+0.5)/len(nodes),
                        45 + depth*78
                    )
                    index[0] += 1
                    position(node.right, depth+1)

                position(self.bst.root)

                def edges(node):
                    if not node:
                        return
                    x, y = coords[node.value]
                    for child in (node.left, node.right):
                        if child:
                            cx, cy = coords[child.value]
                            canvas.create_line(
                                x, y+18, cx, cy-18,
                                fill=t["muted"], width=2
                            )
                            edges(child)

                edges(self.bst.root)

                for node, depth in nodes:
                    x, y = coords[node.value]
                    canvas.create_oval(
                        x-20, y-20, x+20, y+20,
                        fill=t["node"], outline=""
                    )
                    canvas.create_text(
                        x, y, text=str(node.value),
                        fill="white", font=("Segoe UI", 10, "bold")
                    )
                return

            boxw = min(90, max(50, (w-60)/max(1, len(vals))))

            for i, v in enumerate(vals):
                if name == "Stack":
                    x = w/2-boxw/2
                    y = h-45-(i+1)*48
                    canvas.create_rectangle(
                        x, y, x+boxw, y+40,
                        fill=t["node"], outline=t["border"]
                    )
                    canvas.create_text(
                        x+boxw/2, y+20, text=str(v),
                        fill="white", font=("Segoe UI", 11, "bold")
                    )
                else:
                    x = 25+i*boxw
                    y = h/2-22
                    canvas.create_rectangle(
                        x, y, x+boxw-5, y+44,
                        fill=t["node"], outline=t["border"]
                    )
                    canvas.create_text(
                        x+(boxw-5)/2, y+22, text=str(v),
                        fill="white", font=("Segoe UI", 11, "bold")
                    )
                    if name == "Linked List" and i < len(vals)-1:
                        canvas.create_line(
                            x+boxw-5, y+22, x+boxw+7, y+22,
                            arrow=tk.LAST, fill=t["accent"], width=2
                        )

        def log(message):
            history.insert(tk.END, message)
            history.see(tk.END)
            status.configure(text=message)
            draw()

        def operate(action):
            raw = value.get().strip()

            try:
                if action in ("Push", "Enqueue", "Insert"):
                    if not raw:
                        raise ValueError("Enter an integer first.")

                    v = int(raw)

                    if name == "Stack":
                        self.stack.push(v)
                    elif name == "Queue":
                        self.queue.enqueue(v)
                    elif name == "Linked List":
                        self.linked.insert(v)
                    elif name == "Binary Search Tree":
                        self.bst.insert(v)
                    elif name == "B-Tree":
                        self.btree.insert(v)
                    elif name == "Heap":
                        self.heap.push(v)

                    value.set("")
                    log(f"{action}: {v}")

                elif action in ("Pop", "Dequeue", "Extract min"):
                    if name == "Stack":
                        result = self.stack.pop()
                    elif name == "Queue":
                        result = self.queue.dequeue()
                    else:
                        result = self.heap.pop()

                    log(f"{action}: {result}")

                elif action == "Delete":
                    if not raw:
                        raise ValueError("Enter a value to delete.")

                    v = int(raw)

                    if name == "Linked List":
                        result = self.linked.delete(v)
                        log(f"Deleted {v}" if result else f"{v} not found")
                    elif name == "Binary Search Tree":
                        self.bst.delete(v)
                        log(f"Deleted {v} if present")

                elif action == "Search":
                    if not raw:
                        raise ValueError("Enter a value to search for.")

                    v = int(raw)

                    if name == "Linked List":
                        result = self.linked.search(v)
                    elif name == "Binary Search Tree":
                        result = self.bst.search(v)
                    elif name == "B-Tree":
                        result = self.btree.search(v) is not None
                    else:
                        result = v in values_now()

                    log(f"Search {v}: {result}")

            except (ValueError, IndexError) as error:
                messagebox.showerror("Operation failed", str(error))

        operations = {
            "Stack": ["Push", "Pop"],
            "Queue": ["Enqueue", "Dequeue"],
            "Linked List": ["Insert", "Delete", "Search"],
            "Binary Search Tree": ["Insert", "Delete", "Search"],
            "B-Tree": ["Insert", "Search"],
            "Heap": ["Push", "Extract min"]
        }

        for action in operations[name]:
            tk.Button(
                left, text=action,
                command=lambda a=action: operate(a),
                bg=self.theme["button"] if action in (
                    "Push", "Enqueue", "Insert"
                ) else self.theme["soft"],
                fg="white" if action in (
                    "Push", "Enqueue", "Insert"
                ) else self.theme["text"],
                relief="flat", bd=0, pady=8,
                cursor="hand2"
            ).pack(fill="x", padx=14, pady=3)

        canvas.bind("<Configure>", lambda event: draw())
        draw()

    # ==================== AVL VISUALIZER ====================

    def avl_page(self):
        self.heading(
            "AVL Tree",
            "Insert values, inspect balance factors, and explore traversals."
        )

        body = tk.Frame(self.content, bg=self.theme["bg"])
        body.grid(row=1, column=0, sticky="nsew", padx=26, pady=(0, 22))
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = self.card(body)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 14))
        left.configure(width=260)
        left.grid_propagate(False)

        tk.Label(
            left, text="Insert Node", bg=self.theme["panel"],
            fg=self.theme["text"], font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 8))

        value = tk.StringVar()
        entry = tk.Entry(left, textvariable=value, font=("Segoe UI", 11))
        entry.pack(fill="x", padx=14, pady=5, ipady=7)

        canvas = tk.Canvas(
            body, bg=self.theme["canvas"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        canvas.grid(row=0, column=1, sticky="nsew")

        history = tk.Listbox(
            left, height=8, bg=self.theme["panel"],
            fg=self.theme["text"], relief="flat",
            highlightthickness=0
        )
        history.pack(fill="both", expand=True, padx=12, pady=10)

        status = tk.Label(
            left, text="Ready", bg=self.theme["panel"],
            fg=self.theme["muted"], wraplength=230
        )
        status.pack(fill="x", padx=14, pady=8)

        def draw():
            canvas.delete("all")
            w = max(canvas.winfo_width(), 400)
            h = max(canvas.winfo_height(), 300)
            t = self.theme

            for x in range(12, w, 22):
                for y in range(12, h, 22):
                    canvas.create_oval(
                        x, y, x+2, y+2,
                        fill=t["border"], outline=""
                    )

            if not self.avl.root:
                canvas.create_text(
                    w/2, h/2,
                    text="Your AVL tree will appear here",
                    fill=t["muted"], font=("Segoe UI", 13)
                )
                return

            nodes = []
            coords = {}

            def inorder(node, depth=0):
                if not node:
                    return
                inorder(node.left, depth+1)
                nodes.append((node, depth))
                inorder(node.right, depth+1)

            inorder(self.avl.root)
            counter = [0]
            max_depth = max(depth for node, depth in nodes)

            def position(node, depth=0):
                if not node:
                    return
                position(node.left, depth+1)
                coords[node.value] = (
                    35+(w-70)*(counter[0]+0.5)/len(nodes),
                    45+depth*min(85, (h-100)/max(1, max_depth))
                )
                counter[0] += 1
                position(node.right, depth+1)

            position(self.avl.root)

            def draw_edges(node):
                if not node:
                    return
                x, y = coords[node.value]
                for child in (node.left, node.right):
                    if child:
                        cx, cy = coords[child.value]
                        canvas.create_line(
                            x, y+18, cx, cy-18,
                            fill=t["muted"], width=2
                        )
                        draw_edges(child)

            draw_edges(self.avl.root)

            for node, depth in nodes:
                x, y = coords[node.value]
                fill = t["accent"] if node.value == self.last_highlight else t["node"]

                canvas.create_oval(
                    x-21, y-21, x+21, y+21,
                    fill=fill, outline=""
                )
                canvas.create_text(
                    x, y, text=str(node.value),
                    fill="white", font=("Segoe UI", 11, "bold")
                )
                canvas.create_text(
                    x, y+32,
                    text=f"BF {self.avl.balance(node)}",
                    fill=t["muted"], font=("Segoe UI", 8)
                )

        def insert(event=None):
            try:
                v = int(value.get())
                self.avl.insert(v)
                self.last_highlight = v
                history.insert(tk.END, f"Inserted {v}")
                history.see(tk.END)
                status.configure(text=f"Inserted {v}")
                value.set("")
                draw()
            except ValueError as error:
                messagebox.showerror("Cannot insert", str(error))

        entry.bind("<Return>", insert)

        tk.Button(
            left, text="Insert", command=insert,
            bg=self.theme["button"], fg="white",
            relief="flat", bd=0, pady=8
        ).pack(fill="x", padx=14, pady=5)

        for order in ["In-order", "Pre-order", "Post-order"]:
            tk.Button(
                left, text=order,
                command=lambda o=order: messagebox.showinfo(
                    o, " → ".join(map(str, self.avl.traversal(o)))
                    or "Tree is empty"
                ),
                bg=self.theme["soft"], fg=self.theme["text"],
                relief="flat", bd=0, pady=7
            ).pack(fill="x", padx=14, pady=3)

        def clear_tree():
            self.avl = AVLTree()
            self.last_highlight = None
            history.delete(0, tk.END)
            status.configure(text="Tree cleared")
            draw()

        tk.Button(
            left, text="Clear tree", command=clear_tree,
            bg=self.theme["danger"], fg="white",
            relief="flat", bd=0, pady=8
        ).pack(fill="x", padx=14, pady=(8, 14))

        canvas.bind("<Configure>", lambda event: draw())
        draw()

    # ==================== SORTING LAB ====================

    def sorting_page(self):
        self.heading(
            "Sorting Lab",
            "Generate sorting steps and step through comparisons and swaps."
        )

        panel = self.card(self.content)
        panel.grid(row=1, column=0, sticky="nsew", padx=26, pady=(0, 22))
        panel.grid_columnconfigure(0, weight=1)

        top = tk.Frame(panel, bg=self.theme["panel"])
        top.pack(fill="x", padx=16, pady=15)

        self.sort_input = tk.StringVar(value="8, 3, 6, 1, 5, 2")
        tk.Entry(
            top, textvariable=self.sort_input, width=25
        ).pack(side="left", padx=(0, 8), ipady=6)

        self.sort_method = tk.StringVar(value="Bubble Sort")
        tk.OptionMenu(
            top, self.sort_method,
            "Bubble Sort", "Selection Sort", "Insertion Sort",
            "Merge Sort", "Quick Sort"
        ).pack(side="left")

        tk.Button(
            top, text="Generate steps", command=self.run_sort,
            bg=self.theme["button"], fg="white",
            relief="flat", padx=12, pady=8
        ).pack(side="left", padx=8)

        controls = tk.Frame(panel, bg=self.theme["panel"])
        controls.pack(fill="x", padx=16)

        tk.Button(
            controls, text="◀ Previous",
            command=lambda: self.move_sort(-1),
            bg=self.theme["soft"], fg=self.theme["text"],
            relief="flat", padx=12, pady=7
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            controls, text="Next ▶",
            command=lambda: self.move_sort(1),
            bg=self.theme["soft"], fg=self.theme["text"],
            relief="flat", padx=12, pady=7
        ).pack(side="left")

        self.sort_status = tk.Label(
            panel, text="Enter numbers and generate steps.",
            bg=self.theme["panel"], fg=self.theme["muted"]
        )
        self.sort_status.pack(anchor="w", padx=18, pady=10)

        self.sort_canvas = tk.Canvas(
            panel, bg=self.theme["canvas"], height=360,
            highlightthickness=0
        )
        self.sort_canvas.pack(fill="both", expand=True, padx=16, pady=12)

    def run_sort(self):
        try:
            arr = [
                int(x.strip())
                for x in self.sort_input.get().split(",")
                if x.strip()
            ]
            if not arr:
                raise ValueError("Enter at least one number.")
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        functions = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort
        }

        sorted_arr, steps = functions[self.sort_method.get()](arr)
        self.sort_steps = steps + [
            (sorted_arr.copy(), -1, -1, "complete")
        ]
        self.sort_step = 0
        self.draw_sort_step()

    def move_sort(self, delta):
        if not self.sort_steps:
            return
        self.sort_step = max(
            0, min(len(self.sort_steps)-1, self.sort_step+delta)
        )
        self.draw_sort_step()

    def draw_sort_step(self):
        if not self.sort_steps:
            return

        arr, a, b, kind = self.sort_steps[self.sort_step]
        canvas = self.sort_canvas
        canvas.delete("all")

        w = max(canvas.winfo_width(), 350)
        h = max(canvas.winfo_height(), 250)
        max_value = max(arr) if arr else 1
        gap = w/(len(arr)+1)
        bar_width = min(55, gap*.7)

        for i, v in enumerate(arr):
            bar_height = (h-75)*v/max(1, max_value)
            x = (i+1)*gap
            color = (
                self.theme["accent"]
                if i in (a, b) and kind != "complete"
                else self.theme["node"]
            )

            canvas.create_rectangle(
                x-bar_width/2, h-45-bar_height,
                x+bar_width/2, h-45,
                fill=color, outline=""
            )
            canvas.create_text(
                x, h-28, text=str(v),
                fill=self.theme["text"]
            )

        self.sort_status.configure(
            text=f"Step {self.sort_step+1}/{len(self.sort_steps)}"
                 f" · {kind.title()} · Array: {arr}"
        )

    # ==================== SEARCHING LAB ====================

    def searching_page(self):
        self.heading(
            "Searching Lab",
            "Run linear or binary search on a list of integers."
        )

        panel = self.card(self.content)
        panel.grid(row=1, column=0, sticky="new", padx=26)

        row = tk.Frame(panel, bg=self.theme["panel"])
        row.pack(fill="x", padx=18, pady=18)

        numbers = tk.StringVar(value="2, 4, 6, 8, 10, 12")
        target = tk.StringVar(value="8")
        method = tk.StringVar(value="Binary Search")

        tk.Label(
            row, text="Numbers", bg=self.theme["panel"],
            fg=self.theme["text"]
        ).grid(row=0, column=0, sticky="w")

        tk.Entry(
            row, textvariable=numbers, width=28
        ).grid(row=1, column=0, padx=(0, 10), pady=5, ipady=5)

        tk.Label(
            row, text="Target", bg=self.theme["panel"],
            fg=self.theme["text"]
        ).grid(row=0, column=1, sticky="w")

        tk.Entry(
            row, textvariable=target, width=10
        ).grid(row=1, column=1, padx=(0, 10), pady=5, ipady=5)

        tk.OptionMenu(
            row, method, "Linear Search", "Binary Search"
        ).grid(row=1, column=2, padx=5)

        result = tk.Label(
            panel, text="Results will appear here.",
            bg=self.theme["panel"], fg=self.theme["muted"],
            font=("Segoe UI", 11), anchor="w"
        )
        result.pack(fill="x", padx=18, pady=(0, 18))

        def search():
            try:
                arr = [
                    int(x.strip())
                    for x in numbers.get().split(",")
                    if x.strip()
                ]
                key = int(target.get())
            except ValueError:
                messagebox.showerror(
                    "Invalid input", "Enter comma-separated integers and an integer target."
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
                     f" · Index: {index} · Comparisons: {comparisons}"
            )

        tk.Button(
            row, text="Search", command=search,
            bg=self.theme["button"], fg="white",
            relief="flat", padx=15, pady=8
        ).grid(row=1, column=3, padx=8)

    # ==================== GRAPH LAB ====================

    def graph_page(self):
        self.heading(
            "Graph Lab",
            "Create a weighted graph and run BFS, DFS, or Dijkstra's algorithm."
        )

        body = tk.Frame(self.content, bg=self.theme["bg"])
        body.grid(row=1, column=0, sticky="nsew", padx=26, pady=(0, 22))
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = self.card(body)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 14))
        left.configure(width=280)
        left.grid_propagate(False)

        u = tk.StringVar(value="A")
        v = tk.StringVar(value="B")
        weight = tk.StringVar(value="1")

        for label, variable in [
            ("From vertex", u), ("To vertex", v), ("Weight", weight)
        ]:
            tk.Label(
                left, text=label, bg=self.theme["panel"],
                fg=self.theme["muted"]
            ).pack(anchor="w", padx=14, pady=(8, 2))

            tk.Entry(
                left, textvariable=variable
            ).pack(fill="x", padx=14, ipady=5)

        canvas = tk.Canvas(
            body, bg=self.theme["canvas"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        canvas.grid(row=0, column=1, sticky="nsew")

        result = tk.Label(
            left, text="Add edges to create a graph.",
            bg=self.theme["panel"], fg=self.theme["muted"],
            wraplength=245, justify="left"
        )
        result.pack(fill="x", padx=14, pady=10)

        def draw(order=None):
            canvas.delete("all")
            w = max(canvas.winfo_width(), 400)
            h = max(canvas.winfo_height(), 300)
            adj = self.graph.adjacency
            vertices = list(adj)

            for x in range(12, w, 22):
                for y in range(12, h, 22):
                    canvas.create_oval(
                        x, y, x+2, y+2,
                        fill=self.theme["border"], outline=""
                    )

            if not vertices:
                canvas.create_text(
                    w/2, h/2, text="Add edges to visualize your graph",
                    fill=self.theme["muted"], font=("Segoe UI", 12)
                )
                return

            coords = {
                node: (
                    w/2 + min(w, h)*.32*math.cos(2*math.pi*i/len(vertices)),
                    h/2 + min(w, h)*.32*math.sin(2*math.pi*i/len(vertices))
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

                    x1, y1 = coords[a]
                    x2, y2 = coords[b]

                    canvas.create_line(
                        x1, y1, x2, y2,
                        fill=self.theme["muted"], width=2
                    )
                    canvas.create_text(
                        (x1+x2)/2, (y1+y2)/2,
                        text=str(wt), fill=self.theme["text"]
                    )

            for node, (x, y) in coords.items():
                canvas.create_oval(
                    x-22, y-22, x+22, y+22,
                    fill=self.theme["accent"] if order and node in order
                    else self.theme["node"],
                    outline=""
                )
                canvas.create_text(
                    x, y, text=str(node), fill="white",
                    font=("Segoe UI", 11, "bold")
                )

        def add_edge():
            try:
                a, b = u.get().strip(), v.get().strip()
                wt = float(weight.get())

                if not a or not b:
                    raise ValueError("Enter both vertices.")
                if wt < 0:
                    raise ValueError("Use nonnegative weights for this project.")

                self.graph.add_edge(a, b, wt)
                result.configure(text=f"Added edge {a} — {b}, weight {wt:g}")
                draw()

            except ValueError as error:
                messagebox.showerror("Invalid edge", str(error))

        def run_algorithm(kind):
            if not self.graph.adjacency:
                messagebox.showinfo("Empty graph", "Add an edge first.")
                return

            start = u.get().strip()

            try:
                if kind == "BFS":
                    order = self.graph.bfs(start)
                    text = "BFS: " + " → ".join(order)

                elif kind == "DFS":
                    order = self.graph.dfs(start)
                    text = "DFS: " + " → ".join(order)

                else:
                    distances = self.graph.dijkstra(start)
                    order = [
                        n for n, d in distances.items()
                        if d < float("inf")
                    ]
                    text = "Dijkstra: " + ", ".join(
                        f"{n}: {d:g}" if d < float("inf")
                        else f"{n}: ∞"
                        for n, d in distances.items()
                    )

                result.configure(text=text)
                draw(order)

            except ValueError as error:
                messagebox.showerror("Graph error", str(error))

        tk.Button(
            left, text="Add edge", command=add_edge,
            bg=self.theme["button"], fg="white",
            relief="flat", pady=8
        ).pack(fill="x", padx=14, pady=(12, 5))

        for algorithm in ("BFS", "DFS", "Dijkstra"):
            tk.Button(
                left, text=f"Run {algorithm}",
                command=lambda a=algorithm: run_algorithm(a),
                bg=self.theme["soft"], fg=self.theme["text"],
                relief="flat", pady=7
            ).pack(fill="x", padx=14, pady=3)

        canvas.bind("<Configure>", lambda event: draw())
        draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DSAStudio(root)
    root.mainloop()