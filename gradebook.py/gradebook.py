#!/usr/bin/env python3
# Name: Avijit
# Roll No: 2501730308
# Assignment 2 (refactored, using only basic types and functions)

import csv
import os

PASS_MARK = 40.0

def get_manual_input():
    """Collect student marks from user until 'done' is entered."""
    marks = {}
    print("\n--- Manual Data Entry ---")
    print("Type 'done' as name to finish.")
    while True:
        name = input("Enter Student Name: ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("Name cannot be empty.")
            continue
        raw = input(f"Enter marks for {name}: ").strip()
        try:
            score = float(raw)
            if score < 0 or score > 100:
                print("Marks must be between 0 and 100.")
                continue
            marks[name] = score
        except ValueError:
            print("Invalid input. Please enter a number.")
    return marks

def load_csv_data(filename):
    """Load student marks from a CSV file. Expects header with Name,Marks (or simple rows)."""
    marks = {}
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return marks

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Try to detect header: if first row contains non-numeric second column treat as header
            rows = list(reader)
            if not rows:
                return marks

            start_index = 0
            first = rows[0]
            if len(first) >= 2:
                try:
                    float(first[1])
                    # first row is data
                except Exception:
                    # header present
                    start_index = 1

            for row in rows[start_index:]:
                if len(row) < 2:
                    continue
                name = row[0].strip()
                if not name:
                    continue
                try:
                    score = float(row[1].strip())
                    marks[name] = score
                except ValueError:
                    # skip invalid score rows
                    continue

        print(f"Loaded {len(marks)} students from {filename}.")
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")
    return marks

def append_student_record(filename):
    """Append a single student record to a CSV file (create file and header if needed)."""
    name = input("Enter new student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    raw = input("Enter marks (0-100): ").strip()
    try:
        score = float(raw)
        if score < 0 or score > 100:
            print("Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid marks.")
        return

    file_exists = os.path.exists(filename)
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Marks'])
            writer.writerow([name, score])
        print(f"Added {name} to {filename}.")
    except Exception as e:
        print(f"Could not write to '{filename}': {e}")

def calculate_average(marks_dict):
    """Return average of values in marks_dict (0.0 if empty)."""
    if not marks_dict:
        return 0.0
    total = 0.0
    count = 0
    for v in marks_dict.values():
        total += v
        count += 1
    return total / count if count else 0.0

def find_max_score(student_scores):
    """Print highest score and student(s) who achieved it."""
    if not student_scores:
        print("No student data to find max.")
        return
    max_score = None
    max_students = []
    for name, score in student_scores.items():
        if max_score is None or score > max_score:
            max_score = score
            max_students = [name]
        elif score == max_score:
            max_students.append(name)
    names = ", ".join(max_students)
    print(f"HIGHEST SCORE: {max_score} by {names}")

def find_min_score(student_scores):
    """Print lowest score and student(s) who achieved it."""
    if not student_scores:
        print("No student data to find min.")
        return
    min_score = None
    min_students = []
    for name, score in student_scores.items():
        if min_score is None or score < min_score:
            min_score = score
            min_students = [name]
        elif score == min_score:
            min_students.append(name)
    names = ", ".join(min_students)
    print(f"LOWEST SCORE:  {min_score} by {names}")

def assign_grades(student_scores):
    """Return (grades_dict, distribution_dict)."""
    grades = {}
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for name, score in student_scores.items():
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        grades[name] = grade
        distribution[grade] = distribution.get(grade, 0) + 1
    return grades, distribution

def print_summary(student_scores, grades):
    """Print class statistics and a formatted table of each student with grade."""
    if not student_scores:
        print("No student data to show.")
        return

    passed = [n for n, s in student_scores.items() if s >= PASS_MARK]
    failed = [n for n, s in student_scores.items() if s < PASS_MARK]

    print("\n--- Class Statistics ---")
    avg = calculate_average(student_scores)
    print(f"Average Score: {avg:.2f}")

    find_max_score(student_scores)
    find_min_score(student_scores)

    _, final_dist = assign_grades(student_scores)
    print(f"Grade Counts:  {final_dist}")

    print(f"Passed: {len(passed)} students")
    print(f"Failed: {len(failed)} students")

    # Print table header
    print("\n" + "="*50)
    print(f"{'Name':<25} | {'Marks':>6} | {'Grade':>5}")
    print("-" * 50)

    # Keep original insertion order (dict preserves insertion order in Python 3.7+)
    for name, score in student_scores.items():
        grade = grades.get(name, "N/A")
        print(f"{name:<25} | {score:6.1f} | {grade:>5}")

    print("="*50)

def main():
    print("\n=== GRADEBOOK ANALYZER ===")
    while True:
        print("\n1. Manual Entry")
        print("2. Load from CSV")
        print("3. Add Student to CSV")
        print("4. Exit")
        choice = input("Select an option (1-4): ").strip()

        student_scores = {}

        if choice == '1':
            student_scores = get_manual_input()

        elif choice == '2':
            filename = input("Enter CSV filename: ").strip()
            if not filename:
                print("Filename cannot be empty.")
                continue
            student_scores = load_csv_data(filename)

        elif choice == '3':
            filename = input("Enter CSV filename: ").strip()
            if not filename:
                print("Filename cannot be empty.")
                continue
            append_student_record(filename)
            # After appending, reload to show updated data
            student_scores = load_csv_data(filename)

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            continue

        if student_scores:
            final_grades, _ = assign_grades(student_scores)
            print_summary(student_scores, final_grades)
        else:
            if choice in ['1', '2', '3']:
                print("No data loaded.")

if _name_ == "_main_":
    main()