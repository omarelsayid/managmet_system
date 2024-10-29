import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('school.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        grade TEXT,
        registration_date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_name TEXT UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_lessons (
        student_id INTEGER,
        lesson_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
    )
    ''')

    conn.commit()
    conn.close()

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        print("Error: Date must be in the format YYYY-MM-DD.")
        return False

def add_student(student_id, first_name, last_name, age, grade, registration_date):
    if not validate_date(registration_date):
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Ensure unique student_id only
    cursor.execute('SELECT student_id FROM students WHERE student_id = ?', (student_id,))
    if cursor.fetchone():
        print(f"Error: Student ID {student_id} already exists. Please choose a different ID.")
        conn.close()
        return

    # Insert student into the students table
    cursor.execute('''
    INSERT INTO students (student_id, first_name, last_name, age, grade, registration_date)
    VALUES (?, ?, ?, ?, ?, ?)''', (student_id, first_name, last_name, age, grade, registration_date))
    conn.commit()

    # Enroll in lessons if any
    enroll_lessons(student_id, cursor)

    conn.commit()
    conn.close()
    print("Student added successfully with selected lessons!")

def enroll_lessons(student_id, cursor):
    cursor.execute('SELECT lesson_id, lesson_name FROM lessons')
    lessons = cursor.fetchall()
    print("Available Lessons:")
    for lesson in lessons:
        print(f"{lesson[0]}. {lesson[1]}")
    
    lesson_ids = input("Enter the lesson IDs to enroll, separated by commas: ").split(',')

    for lesson_id in lesson_ids:
        try:
            lesson_id = int(lesson_id.strip())
            cursor.execute('INSERT INTO student_lessons (student_id, lesson_id) VALUES (?, ?)', (student_id, lesson_id))
        except ValueError:
            print(f"Invalid lesson ID: {lesson_id}. Skipping this lesson.")
            continue

def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    cursor.execute('DELETE FROM student_lessons WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully!")

def update_student(student_id, first_name, last_name, age, grade, registration_date):
    if not validate_date(registration_date):
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE students SET first_name = ?, last_name = ?, age = ?, grade = ?, registration_date = ?
    WHERE student_id = ?''', (first_name, last_name, age, grade, registration_date, student_id))
    
    update_lessons = input("Do you want to update the lessons for this student? (y/n): ")
    if update_lessons.lower() == 'y':
        cursor.execute('DELETE FROM student_lessons WHERE student_id = ?', (student_id,))
        enroll_lessons(student_id, cursor)

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

    # Check if the lesson name is unique
    cursor.execute('SELECT lesson_name FROM lessons WHERE lesson_name = ?', (lesson_name,))
    if cursor.fetchone():
        print(f"Error: Lesson with name '{lesson_name}' already exists.")
        conn.close()
        return None  # Return None if lesson already exists

    # Insert lesson into the lessons table
    cursor.execute('INSERT INTO lessons (lesson_name) VALUES (?)', (lesson_name,))
    lesson_id = cursor.lastrowid  # Get the ID of the new lesson
    conn.commit()
    conn.close()

    print(f"Lesson '{lesson_name}' added successfully with ID: {lesson_id}!")
    return lesson_id 
    
def delete_lesson(lesson_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lessons WHERE lesson_id = ?', (lesson_id,))
    cursor.execute('DELETE FROM student_lessons WHERE lesson_id = ?', (lesson_id,))
    conn.commit()
    conn.close()
    print("Lesson deleted successfully!")

def update_lesson(lesson_id, new_lesson_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE lessons SET lesson_name = ? WHERE lesson_id = ?', (new_lesson_name, lesson_id))
    conn.commit()
    conn.close()
    print("Lesson updated successfully!")
