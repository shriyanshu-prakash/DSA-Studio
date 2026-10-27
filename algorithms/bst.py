
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        def add(node):
            if node is None:
                return Node(value)

            if value < node.value:
                node.left = add(node.left)
            elif value > node.value:
                node.right = add(node.right)

            return node

        self.root = add(self.root)

    def search(self, value):
        current = self.root

        while current:
            if current.value == value:
                return True
            current = current.left if value < current.value else current.right

        return False

    def inorder(self):
        result = []

        def visit(node):
            if node:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result

    def delete(self, value):
        def remove(node, target):
            if node is None:
                return None

            if target < node.value:
                node.left = remove(node.left, target)
            elif target > node.value:
                node.right = remove(node.right, target)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                successor = node.right
                while successor.left:
                    successor = successor.left

                node.value = successor.value
                node.right = remove(node.right, successor.value)

            return node

        self.root = remove(self.root, value)
