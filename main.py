import os
import tkinter as tk

from algorithms.linked_list import LinkedList
from algorithms.linear_structures import Stack, Queue, MinHeap
from algorithms.bst import BinarySearchTree
from algorithms.btree import BTree
from algorithms.avl import AVLTree
from algorithms.graphs import Graph

from ui.theme import THEMES
from ui.shell import Shell
from ui import (
    dashboard, structures, avl_page, sorting_page, searching_page, graph_page
)

FACTORIES = {
    "Stack": Stack,
    "Queue": Queue,
    "Linked List": LinkedList,
    "Binary Search Tree": BinarySearchTree,
    "AVL Tree": AVLTree,
    "B-Tree": BTree,
    "Heap": MinHeap,
    "Graph Lab": Graph,
}

STRUCTURE_PAGES = (
    "Stack", "Queue", "Linked List", "Binary Search Tree", "B-Tree", "Heap"
)


class DSAStudio:
    def __init__(self, root):
        self.root = root
        self.dark = False
        self.theme = THEMES["light"]
        self.page = "Home"

        # Data structures (one live instance per page)
        self.models = {name: make() for name, make in FACTORIES.items()}

        # UI state that survives page changes and theme toggles
        self.state = {}
        self.tab_memory = {}
        self.sort_state = {
            "steps": [], "step": 0,
            "values": "8, 3, 6, 1, 5, 2", "method": "Bubble Sort"
        }

        root.title("DSA Studio | Algorithm Visualizer")
        root.geometry("1360x820")
        root.minsize(1050, 680)

        self.shell = Shell(self)
        self.content = self.shell.content
        self.show_page("Home")

    # ---------- state ----------

    def reset(self, name):
        self.models[name] = FACTORIES[name]()

    # ---------- navigation ----------

    def toggle_theme(self):
        self.dark = not self.dark
        self.theme = THEMES["dark" if self.dark else "light"]
        self.show_page(self.page)

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, name):
        self.page = name
        self.clear()
        self.shell.set_page(name)
        self.shell.apply_theme(self.theme, self.dark, name)

        if name == "Home":
            dashboard.build(self)
        elif name == "AVL Tree":
            avl_page.build(self)
        elif name in STRUCTURE_PAGES:
            structures.build(self, name)
        elif name == "Sorting":
            sorting_page.build(self)
        elif name == "Searching":
            searching_page.build(self)
        elif name == "Graph Lab":
            graph_page.build(self)
        elif name in ("Data Structures", "Algorithms"):
            dashboard.category(self, name)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "assets", "icon.ico")
    )
    app = DSAStudio(root)
    root.mainloop()