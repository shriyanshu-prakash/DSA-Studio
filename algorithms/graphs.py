
from collections import deque
import heapq


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_edge(self, u, v, weight=1, directed=False):
        self.adjacency.setdefault(u, []).append((v, weight))
        self.adjacency.setdefault(v, [])

        if not directed:
            self.adjacency[v].append((u, weight))

    def bfs(self, start):
        if start not in self.adjacency:
            return []

        visited = {start}
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neighbor, _ in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def dfs(self, start):
        if start not in self.adjacency:
            return []

        visited = set()
        order = []

        def visit(node):
            visited.add(node)
            order.append(node)

            for neighbor, _ in self.adjacency[node]:
                if neighbor not in visited:
                    visit(neighbor)

        visit(start)
        return order

    def dijkstra(self, start):
        if start not in self.adjacency:
            raise ValueError("Starting vertex does not exist.")

        for edges in self.adjacency.values():
            if any(weight < 0 for _, weight in edges):
                raise ValueError("Dijkstra's algorithm requires nonnegative weights.")

        distances = {node: float("inf") for node in self.adjacency}
        distances[start] = 0
        heap = [(0, start)]

        while heap:
            distance, node = heapq.heappop(heap)

            if distance != distances[node]:
                continue

            for neighbor, weight in self.adjacency[node]:
                candidate = distance + weight

                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))

        return distances
