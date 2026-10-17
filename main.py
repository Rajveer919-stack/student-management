# ========== IMPORTS ==========
import sqlite3   # database ke liye (Python mein pehle se hai)


# ========== 1. DATABASE SETUP ==========
# students.db file khud ban jayegi
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Table banao (agar pehle se nahi hai)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        marks REAL
    )
""")
conn.commit()


# ========== 2. STUDENT ADD KARNA ==========
def add_student():
    name = input("Naam: ").strip()
    course = input("Course (BCA/BBA etc): ").strip()

    try:
        marks = float(input("Marks: "))
    except ValueError:
        print("Marks number mein likho!")
        return

    # ? placeholder se data safe tareeke se jata hai
    cursor.execute(
        "INSERT INTO students (name, course, marks) VALUES (?, ?, ?)",
        (name, course, marks),
    )
    conn.commit()
    print("Student add ho gaya!")


# ========== 3. SAARE STUDENTS DEKHNA ==========
def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if not rows:
        print("Abhi koi student nahi hai.")
        return

    print("\nID | Naam | Course | Marks")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")


# ========== 4. NAAM SE SEARCH KARNA ==========
def search_student():
    name = input("Kis naam ko dhundna hai: ").strip()

    # LIKE se aadha naam likhne par bhi mil jata hai
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()

    if not rows:
        print("Koi student nahi mila.")
        return

    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")


# ========== 5. MARKS UPDATE KARNA ==========
def update_marks():
    try:
        student_id = int(input("Student ID: "))
        marks = float(input("Naye marks: "))
    except ValueError:
        print("ID aur marks number mein likho!")
        return

    cursor.execute("UPDATE students SET marks = ? WHERE id = ?", (marks, student_id))
    conn.commit()

    # rowcount = kitni row badli. 0 matlab ID mili hi nahi
    if cursor.rowcount == 0:
        print("Is ID ka student nahi mila.")
    else:
        print("Marks update ho gaye!")


# ========== 6. STUDENT DELETE KARNA ==========
def delete_student():
    try:
        student_id = int(input("Delete karne wale ka ID: "))
    except ValueError:
        print("ID number mein likho!")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Is ID ka student nahi mila.")
    else:
        print("Student delete ho gaya!")


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
        conn.close()   # database band karo
        print("Bye!")
        break
    else:
        print("Galat option, dobara try karo.")