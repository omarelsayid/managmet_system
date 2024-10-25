import sqlite3

def connect_db():
    return sqlite3.connect('school.db')

def create_tables():
    conn = connect_db()    #conect to data base
    cursor = conn.cursor() # create cursor to execute queries 
    

    # Create students table
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

    # Create lessons table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_name TEXT
    )
    ''')

    # Create junction table for many-to-many relationship
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