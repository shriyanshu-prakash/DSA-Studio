class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class LinkedList:
    """Singly linked list by default; optional doubly-linked mode.

    insert(value) appends to the tail for intuitive visualizer behaviour.
    insert(value, position=0) inserts at the head; positive positions insert
    before that index, clamped to the end of the list.
    """
    def __init__(self, doubly=False):
        self.head = None
        self.doubly = doubly
        self.tail = None
        self.length = 0

    def insert(self, value, position=None):
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
            self.length = 1
            return

        # No position means append, matching the UI's Insert button.
        if position is None:
            node.prev = self.tail if self.doubly else None
            self.tail.next = node
            self.tail = node
            self.length += 1
            return

        if position <= 0:
            node.next = self.head
            if self.doubly:
                self.head.prev = node
            self.head = node
            self.length += 1
            return

        current = self.head
        index = 0
        while current.next is not None and index < position - 1:
            current = current.next
            index += 1
        node.next = current.next
        if self.doubly:
            node.prev = current
        current.next = node
        if node.next is not None and self.doubly:
            node.next.prev = node
        if node.next is None:
            self.tail = node
        self.length += 1

    def delete(self, value):
        current = self.head
        previous = None
        while current:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if self.doubly and current.next:
                    current.next.prev = previous
                if self.tail is current:
                    self.tail = previous
                self.length -= 1
                if self.head is None:
                    self.tail = None
                return True
            previous = current
            current = current.next
        return False

    def _last_node(self):
        current = self.head
        if current is None:
            return None
        while current.next:
            current = current.next
        return current

    def search(self, value):
        current, position = self.head, 0
        while current:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return -1

    def values(self):
        result, current = [], self.head
        while current:
            result.append(current.value)
            current = current.next
        return result
