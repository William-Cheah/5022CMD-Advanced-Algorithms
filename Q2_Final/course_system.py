from course_data import build_course_graph
from course import Course

MAX_COURSES = 10    # min = 5, max = 10

#----------------------- input helper -----------------------#
def ask_int(prompt):
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Please enter a whole number.")

def ask_text(prompt):
    """Keep asking until the user type something that is not blank"""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty!")

def ask_int_in_range(prompt, low, high):
    """Keep asking until the user type a whole number from low to high"""
    while True:
        number = ask_int(prompt)
        if low <= number <= high:
            return number
        print(f"Please enter a number from {low} to {high}.")

def ask_level():
    """Keep asking until the user types Care/Elective"""
    while True:
        level = input("Level (Core/Elective): ").strip().capitalize()
        if level in Course.LEVELS:
            return level
        print("Please type Core or Elective.")

def ask_course(catalogue):
    """Ask for a course code and return the matching Course, or None."""
    code = input("Enter Course Code: ").strip().upper()
    course = catalogue.get(code)
    if course is None:
        print(f"Course {code} does not exist.")
    return course

#----------------------- mandatory features -----------------------#
def list_courses(graph):
    """(a) Display a list of all the courses' names."""
    courses = sorted(graph.getVertices(), key=lambda c:c.code)
    print("\nAvailable Courses:")
    for number, course in enumerate(courses, start=1):
        print(f"{number}. {course}")

def view_course_details(catalogue):
    """(b) Show every detail of one course."""
    course = ask_course(catalogue)
    if course is not None:
        print()
        print(course.details())


def view_prerequisites(graph,catalogue):
    """(c) Courses that must be passed first = incoming edges."""
    course = ask_course(catalogue)
    if course is None:
        return
    prerequisites = graph.listIncomingAdjacentVertex(course)
    if not prerequisites:
        print(f"{course} has no prerequisites.")
        return
    print(f"Prerequisites for {course}:")
    for prereq in prerequisites:
        print(f" -{prereq} ")

def view_unlocked_courses(graph,catalogue):
    """(d) Courses this course is a prerequisite for = outgoing edges."""
    course = ask_course(catalogue)
    if course is None:
        return
    unlocked = graph.listOutgoingAdjacentVertex(course)
    if not unlocked:
        print(f"{course} does not unlock any other courses.")
        return
    print(f"Courses unlocked by {course}:")
    for next_course in unlocked:
        print(f" -{next_course}")

def view_course_profile(catalogue):
    """Core: full profile, elective: name only"""
    course = ask_course(catalogue)
    if course is None:
        return
    print()
    if course.is_core():
        print(course.details())
    else:
        print(f"Course Name: {course.name}")
        print(f"(Elective course - other details are hidden)")

#----------------------- advanced feature -----------------------#
def add_course(graph, catalogue):
    """(a) Add a new course (new vertex) on demand."""
    if len(catalogue) >= MAX_COURSES:       # full
        print(f"Cannot add: the system already has {MAX_COURSES} courses.")
        return
    code = ask_text("New Course Code: ").upper()
    if code in catalogue:       # repeated code
        print(f"Course {code} already exists.")
        return
    name = ask_text("Course Name: ")
    credit_hours = ask_int_in_range("Credit Hours (1-6): ", 1,6)
    level = ask_level()
    year = ask_int_in_range("Year (1-3): ",1 , 3)
    try:    # Course validation
        course = Course(code, name,credit_hours, level, year)
    except ValueError as error:
        print(f"{error}. Course not added.")
        return

    graph.addVertex(course)
    catalogue[course.code] = course
    print(f"{course} added successfully. ({len(catalogue)}/{MAX_COURSES} courses)")


#----------------------- helper -----------------------#
def show_links(graph, course):
    """Print a course's current prerequisites and the courses it unlocks"""
    print(f" {course}")
    print(f"    Prerequisites: {graph.listIncomingAdjacentVertex(course) or 'none'}")
    print(f"    Unlocks      : {graph.listOutgoingAdjacentVertex(course) or 'none'}")

#----------------------- advanced feature -----------------------#
def add_prerequisite(graph, catalogue):
    """Course X adds course Y as a prerequisite: new edge Y -> X"""
    print("Course that needs a new prerequisite: ")
    course = ask_course(catalogue)
    if course is None:
        return
    show_links(graph, course)
    print("Prerequisites to add: ")
    prereq = ask_course(catalogue)
    if prereq is None:
        return
    if prereq is course:
        print("A course cannot be a prerequisite of itself.")
    elif graph.hasEdge(prereq, course):
        print(f"{prereq.code} is already a prerequisite of {course.code}")
    elif graph.hasPath(course, prereq):
        #course already leads to prereq, so prereq -> course would close a loop
        print(f"Not added: {course.code} is already needed (directly or "
              f"indirectly) before {prereq.code}. This would create a cycle.")
    else:
        graph.addEdge(prereq, course)
        print(f"{prereq.code} is now a prerequisite of {course.code}.")
        show_links(graph, course)

def remove_prerequisite(graph, catalogue):
    """Course X removes prerequisite Y: delete edge Y -> X"""
    print("Course to remove a prerequisite from: ")
    course = ask_course(catalogue)
    if course is None:
        return
    current = graph.listIncomingAdjacentVertex(course)
    if not current:
        print(f"{course} has no prerequisites to remove.")
        return
    show_links(graph, course)
    print("Prerequisite to remove:")
    prereq = ask_course(catalogue)
    if prereq is None:
        return
    if not graph.hasEdge(prereq, course):
        print(f"{prereq.code} is not a prerequisite of {course.code}.")
        return
    graph.removeEdge(prereq,course)
    print(f"{prereq.code} removed from the prerequisite of {course.code}.")
    show_links(graph, course)

#----------------------- menu -----------------------#
def get_menu_choice():
    print("\n***** University Course Prerequisite System *****")
    print("1. View All Courses")
    print("2. View Course Details")
    print("3. View Prerequisites of a Course")
    print("4. View Courses Unlocked by a Course")
    print("5. Advanced Features")
    print("0. Exit")
    return ask_int("Enter choice: ")

def get_advanced_choice():
    print("\n***** Advanced Features *****")
    print("1. Add a New Course")
    print("2. View Course Profile")
    print("3. Add a Prerequisite to a Course")
    print("4. Remove a Prerequisite from a Course")
    print("0. Back to Main Menu")
    return ask_int("Enter choice: ")

def advanced_menu(graph, catalogue):
    """Sub-menu for the four optional advanced features."""
    while True:
        choice = get_advanced_choice()
        if choice == 1:
            add_course(graph, catalogue)
        elif choice == 2:
            view_course_profile(catalogue)
        elif choice == 3:
            add_prerequisite(graph, catalogue)
        elif choice == 4:
            remove_prerequisite(graph, catalogue)
        elif choice == 0:
            return
        else:
            print("Invalid choice, please enter 0-4")


#----------------------- main -----------------------#
def main():
    graph, catalogue = build_course_graph()
    while True:
        choice = get_menu_choice()
        if choice == 1:
            list_courses(graph)
        elif choice == 2:
            view_course_details(catalogue)
        elif choice == 3:
            view_prerequisites(graph, catalogue)
        elif choice == 4:
            view_unlocked_courses(graph, catalogue)
        elif choice == 5:
            advanced_menu(graph, catalogue)
        elif choice == 0:
            print("Exiting program...")
            break
        else:
            print("Invalid Choice. Please enter 0-5")

if __name__ == "__main__":
    main()


