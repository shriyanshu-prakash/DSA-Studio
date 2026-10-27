
class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, degree=2):
        if degree < 2:
            raise ValueError("B-Tree degree must be at least 2")

        self.degree = degree
        self.root = BTreeNode()

    def search(self, key, node=None):
        node = node or self.root
        i = 0

        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            return node

        if node.leaf:
            return None

        return self.search(key, node.children[i])

    def insert(self, key):
        if self.search(key):
            return

        root = self.root
        max_keys = 2 * self.degree - 1

        if len(root.keys) == max_keys:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_nonfull(self.root, key)

    def _split_child(self, parent, index):
        degree = self.degree
        full = parent.children[index]
        right = BTreeNode(leaf=full.leaf)

        median = full.keys[degree - 1]
        right.keys = full.keys[degree:]
        full.keys = full.keys[:degree - 1]

        if not full.leaf:
            right.children = full.children[degree:]
            full.children = full.children[:degree]

        parent.children.insert(index + 1, right)
        parent.keys.insert(index, median)

    def _insert_nonfull(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(key)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            node.keys[i + 1] = key
            return

        while i >= 0 and key < node.keys[i]:
            i -= 1

        i += 1

        if len(node.children[i].keys) == 2 * self.degree - 1:
            self._split_child(node, i)

            if key > node.keys[i]:
                i += 1

        self._insert_nonfull(node.children[i], key)

    def inorder(self):
        result = []

        def visit(node):
            for i, key in enumerate(node.keys):
                if not node.leaf:
                    visit(node.children[i])
                result.append(key)

            if not node.leaf:
                visit(node.children[len(node.keys)])

        visit(self.root)
        return result
