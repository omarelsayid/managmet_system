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

        try:
            if choice == '1':
                student_id = int(input("Enter student ID: "))
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                age = int(input("Enter age (5-100): "))
                if not (5 <= age <= 100):
                    print("Invalid age. Age must be between 5 and 100.")
                    continue
                grade = input("Enter grade: ")
                registration_date = input("Enter registration date (YYYY-MM-DD): ")
                add_student(student_id, first_name, last_name, age, grade, registration_date)
            elif choice == '2':
                student_id = int(input("Enter student ID to delete: "))
                delete_student(student_id)
            elif choice == '3':
                student_id = int(input("Enter student ID to update: "))
                first_name = input("Enter new first name: ")
                last_name = input("Enter new last name: ")
                age = int(input("Enter new age (5-100): "))
                if not (5 <= age <= 100):
                    print("Invalid age. Age must be between 5 and 100.")
                    continue
                grade = input("Enter new grade: ")
                registration_date = input("Enter new registration date (YYYY-MM-DD): ")
                update_student(student_id, first_name, last_name, age, grade, registration_date)
            elif choice == '4':
                student_id = int(input("Enter student ID to display: "))
                display_student(student_id)
            elif choice == '5':
                lesson_name = input("Enter lesson name: ")
                add_lesson(lesson_name)
            elif choice == '6':
                lesson_id = int(input("Enter lesson ID to delete: "))
                delete_lesson(lesson_id)
            elif choice == '7':
                lesson_id = int(input("Enter lesson ID to update: "))
                new_lesson_name = input("Enter new lesson name: ")
                update_lesson(lesson_id, new_lesson_name)
            elif choice == '8':
                print("Exiting the program...")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

if __name__ == "__main__":
    main_menu()