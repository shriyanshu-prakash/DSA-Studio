class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        # Every rotation performed, as (direction, value of the node rotated)
        self.rotations = []

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        self.rotations.append(("Right", y.value))
        x = y.left
        middle = x.right
        x.right = y
        y.left = middle

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def rotate_left(self, x):
        self.rotations.append(("Left", x.value))
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

    def size(self):
        return len(self.traversal("In-order"))

    def tree_height(self):
        return self.height(self.root)