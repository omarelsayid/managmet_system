from create_database import connect_db, create_tables


def add_student(student_id, first_name, last_name, age, grade, registration_date, lessons):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert student into the students table
    cursor.execute('''
    INSERT INTO students (student_id, first_name, last_name, age, grade, registration_date)
    VALUES (?, ?, ?, ?, ?, ?)''', (student_id, first_name, last_name, age, grade, registration_date))
    conn.commit()

    for lesson in lessons:
        # Check if the lesson exists
        cursor.execute('SELECT lesson_id FROM lessons WHERE lesson_name = ?', (lesson,))
        lesson_result = cursor.fetchone()
        
        if lesson_result:
            lesson_id = lesson_result[0]  # Use the existing lesson_id
        else:
            # If the lesson doesn't exist, create it
            cursor.execute('INSERT INTO lessons (lesson_name) VALUES (?)', (lesson,))
            lesson_id = cursor.lastrowid  # Get the ID of the newly added lesson

        # Enroll the student in the lesson
        cursor.execute('INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)', (student_id, lesson_id))

    conn.commit()
    conn.close()
    print("Student added successfully with lessons!")

def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully!")

def update_student(student_id, first_name, last_name, age, grade, registration_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE students SET first_name = ?, last_name = ?, age = ?, grade = ?, registration_date = ?
    WHERE student_id = ?''', (first_name, last_name, age, grade, registration_date, student_id))
    conn.commit()
    conn.close()
    print("Student updated successfully!")

def display_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()

    if student:
        print(f"Student ID: {student[0]}\nFirst Name: {student[1]}\nLast Name: {student[2]}\nAge: {student[3]}\nGrade: {student[4]}\nRegistration Date: {student[5]}")
        
        # Fetching enrolled lessons
        cursor.execute('''
        SELECT lessons.lesson_name FROM lessons
        JOIN student_lessons ON lessons.lesson_id = student_lessons.lesson_id
        WHERE student_lessons.student_id = ?
        ''', (student_id,))
        
        enrolled_lessons = cursor.fetchall()
        if enrolled_lessons:
            print("Enrolled Lessons:")
            for lesson in enrolled_lessons:
                print(f"- {lesson[0]}")
        else:
            print("No lessons enrolled.")
    else:
        print("Student not found!")
    conn.close()

def add_lesson(lesson_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lessons (lesson_name) VALUES (?)', (lesson_name,))
    conn.commit()
    conn.close()
    print("Lesson added successfully!")

# Example menu interface
def main_menu():
    create_tables()  # Ensure tables are created at the start

    while True:
        print("""
        Please choose an operation:
        1. Add a student
        2. Delete a student
        3. Update a student's information
        4. Display a student's information
        5. Add a lesson
        6. Quit
        """)

        choice = input("Your choice: ")
        if choice == '1':
            # Collect student details and lessons
            student_id = int(input("Enter student ID: "))
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: "))
            grade = input("Enter grade: ")
            registration_date = input("Enter registration date (YYYY-MM-DD): ")
            lessons = input("Enter lessons separated by commas: ").split(',')
            add_student(student_id, first_name, last_name, age, grade, registration_date, [lesson.strip() for lesson in lessons])
        elif choice == '2':
            student_id = int(input("Enter student ID to delete: "))
            delete_student(student_id)
        elif choice == '3':
            student_id = int(input("Enter student ID to update: "))
            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")
            age = int(input("Enter new age: "))
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
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()