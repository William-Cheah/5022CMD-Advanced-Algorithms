# Q2 – Graph: University Course Prerequisite System

An unweighted directed graph stored as two adjacency-list dictionaries
(outgoing and incoming edges). Each course is a vertex and an edge points from
a prerequisite to the course it unlocks, so the prerequisites of a course are
its incoming edges and the courses it unlocks are its outgoing edges.

## Files

| File | Purpose |
|---|---|
| `graph.py` | Generic `Graph` class: addVertex, addEdge, listIncomingAdjacentVertex, listOutgoingAdjacentVertex, getVertices, hasEdge, removeEdge, hasPath (breadth-first search) |
| `course.py` | `Course` entity class with validation |
| `course_data.py` | Eight pre-defined courses and nine prerequisite links |
| `course_system.py` | Main menu (mandatory features a–d) and advanced sub-menu (add course, course profile, add / remove prerequisite with cycle check) |
| `test_graph.py` | Uses the same `Graph` class with plain strings to show that it is generic |

## How to run

```
python course_system.py   # the course prerequisite system
python test_graph.py      # Graph class used on its own
```
