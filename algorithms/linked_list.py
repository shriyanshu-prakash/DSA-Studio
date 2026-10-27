
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self, doubly=False):
        self.head = None
        self.doubly = doubly

    def insert(self, value, position=None):
        node = Node(value)

        if self.head is None:
            self.head = node
            return

        if position is None or position <= 0:
            node.next = self.head
            if self.doubly:
                self.head.prev = node
            self.head = node
            return

        current = self.head
        for _ in range(position - 1):
            if current.next is None:
                break
            current = current.next

        node.next = current.next
        if self.doubly:
            node.prev = current
        current.next = node

        if self.doubly and node.next:
            node.next.prev = node

    def delete(self, value):
        current = self.head

        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next and self.doubly:
                    current.next.prev = current.prev

                return True

            current = current.next

        return False

    def search(self, value):
        current = self.head
        position = 0

        while current:
            if current.value == value:
                return position
            current = current.next
            position += 1

        return -1

    def values(self):
        result = []
        current = self.head

        while current:
            result.append(current.value)
            current = current.next

        return result
