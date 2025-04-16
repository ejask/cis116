"""
File name: hw04.py
Author: Emma Jaskowiec
Section: E
Description: Takes, as user input, a number of students, a number of assignments, and each student's scores on each assignment. Prints a grade report including each student's grade and each assignment's average score (both in percentage and letter format).
"""


def add_student(students: dict[str, dict]) -> None:
    """Appends a new dictionary representing a student (values depending on user input) to the input dictionary."""
    name = input("Student name: ").strip()
    students[input("Student ID: ").strip()] = {"Name": name}


def input_assignments(student: dict, num_assignments: int) -> None:
    """Given a dictionary representing a student, asks the user for the student's scores (as floats from 0-100) on each of the given number of assignments, then appends the resulting list to the student dictionary."""
    print(f"Enter the scores for {student['Name']}")
    scores = []

    for i in range(num_assignments):
        while True:
            # Assignments are zero-indexed internally; we print a shifted value here to make indexing more intuitive to the user.
            score = input(f"Enter score (0-100) for assignment {i + 1}: ").strip()

            # Handle inputs that aren't valid floats
            try:
                score = float(score)
            except ValueError:
                print("Invalid input; expected an integer or decimal number")
                continue

            # Handle inputs outside the valid range
            if score <= 100 and score >= 0:
                scores.append(score)
                break  # Input is valid; end loop
            else:
                print("Invalid input; expected a number 0-100")

    student["Scores"] = scores


def grade_student(student: dict) -> None:
    """Calculates the average grade of the given student dictionary and stores it in the dictionary."""
    sum = 0
    for score in student["Scores"]:
        sum += score
    student["Grade"] = sum / len(student["Scores"])


def get_letter_grade(score: float) -> str:
    """Return the letter grade that corresponds to the given percentage grade."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def print_report(students: dict[str, dict], num_assignments: int) -> None:
    """Given a dictionary of students, print the grade report for each student."""
    # The array needs to be initialized for use of the += operator
    averages = [0] * num_assignments

    # Print student grades
    print("Final grade report:")
    for student in students.values():
        print(
            f"{student['Name']}'s average score was {student['Grade']:.1f}, letter grade of {get_letter_grade(student['Grade'])}"
        )
        # Add to sum of scores for each assignment
        for i in range(num_assignments):
            averages[i] += student["Scores"][i]

    # Take the average
    num_students = len(students)
    averages = [score / num_students for score in averages]

    # Print assignment averages
    print("\nAssignment averages:")
    for i, score in enumerate(averages):
        print(
            f"The average for assignment {i + 1} was {score:.1f}, letter grade of {get_letter_grade(score)}"
        )


def main():
    # Initialize student dictionary
    students = {}

    # Student input loop
    while True:
        add_student(students)
        print()
        choice = input("Enter another student? (y)es/(n)o: ").strip().lower()
        print()
        if not (choice == "y" or choice == "yes"):
            break

    # Get number of assignments (integer greater than 0)
    num_assignments = 0
    while True:
        num_assignments = input("Number of assignments: ").strip()
        try:
            num_assignments = int(num_assignments)
        except ValueError:
            print("Invalid input; expected an integer")
            continue
        if num_assignments > 0:
            print()
            break  # Input is valid; end loop
        else:
            print("Invalid input; expected a number greater than 0")

    # Input assignments and grade students
    for student in students.values():
        input_assignments(student, num_assignments)
        grade_student(student)
        print()

    # Print results
    print_report(students, num_assignments)


if __name__ == "__main__":
    main()
