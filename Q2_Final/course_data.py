from course import Course
from graph import Graph

def build_course_graph():
    """Create the course objects and the prerequisite graph
    Returns (graph, catalogue), where catalogue maps course code -> Course."""
    courses = [
        Course("CS101", "Introduction to Programming", 4, "Core", 1),
        Course("CS102", "Discrete Mathematics", 3, "Core", 1),
        Course("CS201", "Data Structures", 4, "Core", 2),
        Course("CS202", "Database Systems", 3, "Core", 2),
        Course("CS203", "Web Development", 3, "Elective", 2),
        Course("CS301", "Algorithms", 4, "Core", 3),
        Course("CS302", "Machine Learning", 3, "Elective", 3),
        Course("CS303", "Software Engineering", 4, "Core", 3),
    ]

    graph = Graph()
    catalogue = {}
    for course in courses:
        graph.addVertex(course)
        catalogue[course.code] = course

    # (prerequisite, course): the first must be passed before the second
    prerequisites = [
        ("CS101","CS201"),("CS101","CS202"),("CS101","CS203"),
        ("CS102", "CS301"), ("CS102", "CS302"),
        ("CS201", "CS301"), ("CS201", "CS302"),("CS201","CS303"),
        ("CS202", "CS303")
    ]
    for before, after in prerequisites:
        graph.addEdge(catalogue[before], catalogue[after])

    return graph, catalogue

