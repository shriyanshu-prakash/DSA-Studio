
class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items.pop()

    def peek(self):
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items[-1]

    def values(self):
        return self.items[::-1]


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if not self.items:
            raise IndexError("Queue is empty")
        return self.items.pop(0)

    def peek(self):
        if not self.items:
            raise IndexError("Queue is empty")
        return self.items[0]

    def values(self):
        return self.items.copy()


class MinHeap:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)
        i = len(self.items) - 1

        while i > 0:
            parent = (i - 1) // 2
            if self.items[parent] <= self.items[i]:
                break
            self.items[parent], self.items[i] = (
                self.items[i], self.items[parent]
            )
            i = parent

    def pop(self):
        if not self.items:
            raise IndexError("Heap is empty")

        self.items[0], self.items[-1] = (
            self.items[-1], self.items[0]
        )
        result = self.items.pop()
        i = 0

        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < len(self.items) and self.items[left] < self.items[smallest]:
                smallest = left

            if right < len(self.items) and self.items[right] < self.items[smallest]:
                smallest = right

            if smallest == i:
                break

            self.items[i], self.items[smallest] = (
                self.items[smallest], self.items[i]
            )
            i = smallest

        return result
