from collections import deque

class Graph:
    """Unweighted directed graph stored as an adjacency list"""

    def __init__(self):
        self.outgoing = {}  # vertex -> vertices it points to (going)
        self.incoming = {}  # vertex -> vertices that point to it (coming)

    def addVertex(self, vertex):
        if vertex not in self.outgoing:
            self.outgoing[vertex] = []
            self.incoming[vertex] = []

    def addEdge(self, from_vertex, to_vertex):
        # both vertices must exist
        if from_vertex not in self.outgoing or to_vertex not in self.outgoing:
            raise ValueError("Both vertices must be added before the edge")
        # same edge cannot add twice
        if to_vertex not in self.outgoing[from_vertex]:
            self.outgoing[from_vertex].append(to_vertex)    # "FROM" unlock "TO"
            self.incoming[to_vertex].append(from_vertex)    # Prerequisite of "TO" is "FROM"

    def listIncomingAdjacentVertex(self, vertex):
        if vertex not in self.incoming:
            raise ValueError(f"Vertex {vertex} not in the graph")
        return list(self.incoming[vertex])    # Encapsulation: give a copy of list

    def listOutgoingAdjacentVertex(self, vertex):
        if vertex not in self.outgoing:
            raise ValueError(f"Vertex {vertex} is not in the graph")
        return list(self.outgoing[vertex])

    def getVertices(self):
        return list(self.outgoing.keys())

    def display(self):
        for vertex in self.outgoing:
            # !r = use __repr__ to show
            print(f"{vertex!r} out -> {self.outgoing[vertex]}, in <- {self.incoming[vertex]}")

    # for advanced feature: add/delete prerequisite
    def hasEdge(self, from_vertex, to_vertex):
        """True if the edge from_vertex -> to_vertex exists"""
        return from_vertex in self.outgoing and to_vertex in self.outgoing[from_vertex]

    def removeEdge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex from BOTH dictionaries"""
        if not self.hasEdge(from_vertex, to_vertex):
            raise ValueError(f"Edge {from_vertex} -> {to_vertex} not in the graph")
        self.outgoing[from_vertex].remove(to_vertex)
        self.incoming[to_vertex].remove(from_vertex)

    def hasPath(self, start, goal):
        """Breadth-first search: True if goal can be reached from start"""
        if start not in self.outgoing or goal not in self.outgoing:
            raise ValueError("Both vertices must be in the graph")
        visited = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex == goal:
                return True
            for neighbour in self.outgoing[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False

# queue = [CS101]                visited = {CS101}
# take CS101 → neighbour: CS201, CS202, CS203, put in queue
# queue = [CS201, CS202, CS203]
# take CS201 → neighbour CS301, CS302, CS303, put in queue
# queue = [CS202, CS203, CS301, CS302, CS303]
# take CS202 → neighbour CS303 already visited skip
# take CS203 → no neighbour
# take CS301 → is goal！ return True