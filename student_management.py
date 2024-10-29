from create_database import (
    create_tables,
    add_student,
    delete_student,
    update_student,
    display_student,
    add_lesson,
    delete_lesson,
    update_lesson
)
from datetime import datetime

def validate_date(date_text):
    """Validates that the date is in the format YYYY-MM-DD."""
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main_menu():
    create_tables()

    while True:
        print("""
        Please choose an operation:
        1. Add a student
        2. Delete a student
        3. Update a student's information
        4. Display a student's information
        5. Add a lesson
        6. Delete a lesson
        7. Update a lesson's name
        8. Quit
        """)

        choice = input("Your choice: ")

        if choice == '1':
            while True:
                try:
                    student_id = int(input("Enter student ID: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student ID (number).")

            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            
            while True:
                try:
                    age = int(input("Enter age (5-100): "))
                    if 5 <= age <= 100:
                        break
                    else:
                        print("Invalid age. Age must be between 5 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid age (number).")

            grade = input("Enter grade: ")

            while True:
                registration_date = input("Enter registration date (YYYY-MM-DD): ")
                if validate_date(registration_date):
                    break
                else:
                    print("Invalid date format. Please use the format YYYY-MM-DD.")

            add_student(student_id, first_name, last_name, age, grade, registration_date)

        elif choice == '2':
            while True:
                try:
                    student_id = int(input("Enter student ID to delete: "))
                    delete_student(student_id)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student ID.")

        elif choice == '3':
            while True:
                try:
                    student_id = int(input("Enter student ID to update: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student ID.")
            
            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")

            while True:
                try:
                    age = int(input("Enter new age (5-100): "))
                    if 5 <= age <= 100:
                        break
                    else:
                        print("Invalid age. Age must be between 5 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid age (number).")

            grade = input("Enter new grade: ")

            while True:
                registration_date = input("Enter new registration date (YYYY-MM-DD): ")
                if validate_date(registration_date):
                    break
                else:
                    print("Invalid date format. Please use the format YYYY-MM-DD.")

            update_student(student_id, first_name, last_name, age, grade, registration_date)

        elif choice == '4':
            while True:
                try:
                    student_id = int(input("Enter student ID to display: "))
                    display_student(student_id)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid student ID.")

        elif choice == '5':
            lesson_name = input("Enter lesson name: ")
            add_lesson(lesson_name)

        elif choice == '6':
            while True:
                try:
                    lesson_id = int(input("Enter lesson ID to delete: "))
                    delete_lesson(lesson_id)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid lesson ID.")

        elif choice == '7':
            while True:
                try:
                    lesson_id = int(input("Enter lesson ID to update: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid lesson ID.")

            new_lesson_name = input("Enter new lesson name: ")
            update_lesson(lesson_id, new_lesson_name)

        elif choice == '8':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
