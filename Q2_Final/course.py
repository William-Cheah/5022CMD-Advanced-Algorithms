class Course:
    """One course offered by the university"""
    LEVELS = ("Core", "Elective")

    def __init__(self, code, name, credit_hours, level, year):
        # validation
        if not code.strip():
            raise ValueError("Course code cannot be empty")
        if not name.strip():
            raise ValueError("Course name cannot be empty")
        if credit_hours <= 0:
            raise ValueError("Credit hours must be a positive number")
        if level not in Course.LEVELS:
            raise ValueError("Level must be 'Core' or 'Elective'")
        if year not in (1,2,3):
            raise ValueError("Year must be 1, 2, or 3")

        # attributes
        self.code = code.strip().upper()    # str, such as "CS201"
        self.name = name.strip()            # str
        self.credit_hours = credit_hours    # int
        self.level = level                  # str: "Core" or "Elective"
        self.year = year                    # int: year of study

    def is_core(self):
        return self.level == "Core"

    def details(self):
        return (f"Course Code : {self.code}\n"
                f"Course Name : {self.name}\n"
                f"Credit Hours: {self.credit_hours}\n"
                f"Level       : {self.level}\n"
                f"Year        : {self.year}")

    def __str__(self):
        return f"{self.code} -> {self.name}"

    def __repr__(self):     # use to print a list
        return self.code
