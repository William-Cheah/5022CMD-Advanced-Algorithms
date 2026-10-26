"""Shows that Graph is generic: it works with plain strings, not only Course objects."""
from graph import Graph

roads = Graph()
for town in ["A", "B", "C", "D"]:
    roads.addVertex(town)

roads.addEdge("A", "B")       # one-way roads
roads.addEdge("B", "C")
roads.addEdge("C", "A")       # a cycle is allowed in a general graph

print("Roads into A   :", roads.listIncomingAdjacentVertex("A"))
print("Roads out of B :", roads.listOutgoingAdjacentVertex("B"))
print("A can reach C  :", roads.hasPath("A", "C"))
print("A can reach D  :", roads.hasPath("A", "D"))

roads.removeEdge("C", "A")
print("After removing C -> A, roads into A:", roads.listIncomingAdjacentVertex("A"))

try:
    roads.addEdge("A", "Z")
except ValueError as error:
    print("Error caught   :", error)



