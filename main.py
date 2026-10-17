# ========== IMPORTS ==========
import sqlite3   # for the database (comes with Python)


# ========== 1. DATABASE SETUP ==========
# The students.db file is created automatically
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the table if it does not exist yet
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        marks REAL
    )
""")
conn.commit()


# ========== 2. ADD A STUDENT ==========
def add_student():
    name = input("Name: ").strip()
    course = input("Course (BCA/BBA etc): ").strip()

    try:
        marks = float(input("Marks: "))
    except ValueError:
        print("Please enter marks as a number!")
        return

    # The ? placeholders send data safely (prevents SQL injection)
    cursor.execute(
        "INSERT INTO students (name, course, marks) VALUES (?, ?, ?)",
        (name, course, marks),
    )
    conn.commit()
    print("Student added!")


# ========== 3. VIEW ALL STUDENTS ==========
def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if not rows:
        print("No students yet.")
        return

    print("\nID | Name | Course | Marks")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")


# ========== 4. SEARCH BY NAME ==========
def search_student():
    name = input("Enter the name to search: ").strip()

    # LIKE also matches part of a name
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()

    if not rows:
        print("No student found.")
        return

    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")


# ========== 5. UPDATE MARKS ==========
def update_marks():
    try:
        student_id = int(input("Student ID: "))
        marks = float(input("New marks: "))
    except ValueError:
        print("Please enter the ID and marks as numbers!")
        return

    cursor.execute("UPDATE students SET marks = ? WHERE id = ?", (marks, student_id))
    conn.commit()

    # rowcount = number of rows changed; 0 means the ID was not found
    if cursor.rowcount == 0:
        print("No student found with this ID.")
    else:
        print("Marks updated!")


# ========== 6. DELETE A STUDENT ==========
def delete_student():
    try:
        student_id = int(input("ID of the student to delete: "))
    except ValueError:
        print("Please enter the ID as a number!")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("No student found with this ID.")
    else:
        print("Student deleted!")


# ========== 7. MAIN MENU ==========
while True:
    print("\n1. Add  2. View  3. Search  4. Update Marks  5. Delete  6. Exit")
    choice = input("Choose: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_marks()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        conn.close()   # close the database
        print("Bye!")
        break
    else:
        print("Invalid option, please try again.")