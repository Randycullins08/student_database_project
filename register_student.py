import sqlite3
from datetime import date
from getpass import getpass

connection = sqlite3.connect('my_student_data.db')
cursor = connection.cursor()

def create_person():
    print()
    print("Enter Persons Information")
    first_name = input("Enter First Name: ").title()
    last_name = input("Enter Last Name: ").title()
    email = input("Enter Email Address: ")
    phone = input("Enter Phone Number: ")
    password = getpass("Enter Password: ")
    address = input("Enter Street Address: ").title()
    city = input("Enter City Location: ").title()
    state = input("Enter State Location: ").upper()
    postal_code = input("Enter Postal Code: ")
    person_info = [
                (first_name, last_name, email, phone, password, address, city, state, postal_code)
            ]
    insert_sql = "INSERT INTO People(first_name, last_name, email, phone, password, address, city, state, postal_code) VALUES(?,?,?,?,?,?,?,?,?)"
    for person in person_info:
        cursor.execute(insert_sql, person)
    print()
    print(f"{first_name} has been added")
    print()
    connection.commit()
    active_people()

def create_course():    
    print()
    print("Enter Course Information")
    name = input("Enter Name of Course: ").title()
    description = input("Enter Course Description: ").title()
    course_info = [
                (name, description)
            ]
    insert_sql = "INSERT INTO Courses(name, description) VALUES(?,?)"
    for course in course_info:
        cursor.execute(insert_sql, course)
    print(f"Course {name} has been added")
    connection.commit()
    active_course()


def create_cohort():
    print()
    person_print = cursor.execute("SELECT person_id, first_name FROM People WHERE active = 1").fetchall()
    courses_print = cursor.execute("SELECT course_id, name FROM Courses WHERE active = 1").fetchall()
    print("Select The Instructor: ")
    print()
    for person in person_print:
        print(f"{person[0]}. {person[1]}")
    print() 
    instructor_id = input("Enter Instructor ID: ")
    print()
    print("Select Which Course: ")
    for course in courses_print:
        print(f"{course[0]}. {course[1]}")
    print()
    course_id_input = input("Enter Course ID: ")
    start_date_input = date.today()
    query= 'INSERT INTO Cohort(instructor_id, course_id, start_date, end_date) VALUES(?,?,?,?)'
    values = (instructor_id, course_id_input, start_date_input, "2021-12-10")
    cursor.execute(query, values)
    print("Cohort was created")
    connection.commit()
    active_cohort()

def student_registration():
    print()
    active_people()
    print()
    student_id = input("Enter Person ID: ")
    print()
    print("Select the cohort to register them to: ")
    active_cohort()
    cohort_id = input("Enter Cohort ID: ")
    register_date = date.today()
    query = "INSERT INTO Student_Cohort_Registration(student_id, cohort_id, registration_date) VALUES(?,?,?)"
    values = (student_id, cohort_id, register_date)
    cursor.execute(query, values)
    print(f"Student was registered to cohort {cohort_id}")
    connection.commit()

def remove_student():
    print()
    scr_print_table()
    print()
    student_id = input("Enter Student ID to be removed: ")
    drop_date = date.today()
    query = "UPDATE Student_Cohort_Registration SET active = 0, drop_date = ? WHERE student_id = ?;"
    values = (drop_date, student_id)
    cursor.execute(query, values)
    print("Student was removed")
    connection.commit()

def course_deactivate():
    print()
    active_course()
    course_select = input("Enter Course ID: ")
    query = "UPDATE Courses SET active = 0 WHERE course_id = ?"
    value = (course_select)
    cursor.execute(query, (value,))
    print("Course has been removed")
    connection.commit()

def course_reactivate():
    print()
    not_active_course()
    course_select = input("Enter Course ID: ")
    query = "UPDATE Courses SET active = 1 WHERE course_id = ?"
    value = ((course_select,))
    cursor.execute(query, value)
    print("Course has been reactivated")
    connection.commit()

def person_deactivate():
    print()
    active_people()
    print()
    person_select = (input("Enter Person ID: "))
    query = "UPDATE People SET active = 0 WHERE person_id = ?"
    value = ((person_select,))
    cursor.execute(query, value)
    print()
    print(f"{person_select} has been removed")
    connection.commit()
    active_people()

def person_reactivate():
    print()
    not_active_people()
    print()
    person_select = input("Enter Person ID: ")
    query = "UPDATE People SET active = 1 WHERE person_id = ?"
    value = (person_select)
    cursor.execute(query, (value,))
    print()
    print(f"{person_select} has been reactivated")
    connection.commit()
    
def cohort_deactivate():
    print()
    active_cohort()
    cohort_select = input("Enter Cohort ID To Deactivate: ")
    query = "UPDATE Cohort SET active = 0 WHERE cohort_id = ?"
    value = ((cohort_select,))
    cursor.execute(query, value)
    print("Cohort has been removed")
    connection.commit()

def cohort_reactivate():
    print()
    not_active_cohort()
    cohort_select = input("Enter Cohort ID To Reactivate: ")
    query = "UPDATE Cohort SET active = 1 WHERE cohort_id = ?"
    value = ((cohort_select,))
    cursor.execute(query, value)
    print("Cohort has been reactivated")
    connection.commit()

def student_completion():
    print()
    scr_print_table()
    print()
    student_select = input("Enter student to select: ")
    completion_date = date.today()
    query = "UPDATE Student_Cohort_Registration SET completion_date = ?, active = 0 WHERE cohort_id = ?"
    values = (completion_date, student_select)
    cursor.execute(query, values)
    print("Student has completed the course!")
    connection.commit()

def student_reactivation():
    print()
    deactive_scr_table()
    print()
    student_select = input("Enter student to select: ")
    query = "UPDATE Student_Cohort_Registration SET completion_date = NULL, drop_date = NULL, active = 1 WHERE cohort_id = ?"
    values = (student_select)
    cursor.execute(query, (values,))
    print("Student has been reactivated")
    connection.commit()

def active_cohort():
    print()
    cohort_print = cursor.execute("SELECT * FROM Cohort WHERE active = 1").fetchall()
    for cohort in cohort_print:
        print()
        print(f"{'Student ID':<12}{'Cohort ID':<11}{'Course ID':<11}{'Completion Date':<17}{'Drop Date':<11}{'Active':>9}")
        print("-" * 71)
        print(f"{cohort[0]:<12}{cohort[1]:<11}{cohort[2]:<11}{cohort[3]:<17}{cohort[4]:<11}{cohort[5]:>9} \n")

def not_active_cohort():
    print()
    cohort_print = cursor.execute("SELECT * FROM Cohort WHERE active = 0").fetchall()
    for cohort in cohort_print:
        print()
        print(f"{'Student ID':<12}{'Cohort ID':<11}{'Course ID':<11}{'Completion Date':<17}{'Drop Date':<11}{'Active':>9}")
        print("-" * 71)
        print(f"{cohort[0]:<12}{cohort[1]:<11}{cohort[2]:<11}{cohort[3]:<17}{cohort[4]:<11}{cohort[5]:>9} \n")

def active_course():
    print()
    course_print = cursor.execute("SELECT * FROM Courses WHERE active = 1").fetchall()
    for course in course_print:
        print()
        print(f"{'Course ID':<11}{'Name':<12}{'Decription':<30}{'Active':>8}")
        print("-" * 61)
        print(f"{course[0]:<11}{course[1]:<12}{course[2]:<30}{course[3]:>8}\n")

def not_active_course():
    print()
    course_print = cursor.execute("SELECT * FROM Courses WHERE active = 0").fetchall()
    for course in course_print:
        print()
        print(f"{'Course ID':<11}{'Name':<12}{'Decription':<30}{'Active':>8}")
        print("-" * 61)
        print(f"{course[0]:<11}{course[1]:<12}{course[2]:<30}{course[3]:>8}\n")

def active_people():
    print()
    people_print = cursor.execute("SELECT * FROM People WHERE active = 1").fetchall()
    for people in people_print:
        print()
        print(f"{'Person ID':11}{'First Name':<15}{'Last Name':<15}{'Email':<25}{'Phone':<14}{'Address':<20}{'City':<10}{'State':<7}{'Postal Code':<12}{'Active':>10}")
        print("-" * 139)
        print(f"{people[0]:<11}{people[1]:<15}{people[2]:<15}{people[3]:<25}{people[4]:<14}{people[6]:<20}{people[7]:<10}{people[8]:<7}{people[9]:<12}{people[10]:>10}")

def not_active_people():
    print()
    people_print = cursor.execute("SELECT * FROM People WHERE active = 0").fetchall()
    for people in people_print:
        print()
        print(f"{'Person ID':11}{'First Name':<15}{'Last Name':<15}{'Email':<25}{'Phone':<14}{'Address':<20}{'City':<10}{'State':<7}{'Postal Code':<12}{'Active':>10}")
        print("-" * 139)
        print(f"{people[0]:<11}{people[1]:<15}{people[2]:<15}{people[3]:<25}{people[4]:<14}{people[6]:<20}{people[7]:<10}{people[8]:<7}{people[9]:<12}{people[10]:>10}")

def scr_print_table():
    table_print = cursor.execute("SELECT * FROM Student_Cohort_Registration WHERE active = 1").fetchall()
    for table in table_print:
        print()
        print(f"{'Student ID':<12}{'Cohort ID':<11}{'Registration Date':<19}{'Active':>8}")
        print("-" * 50)
        print(f"{table[0]:<12}{table[1]:<11}{table[2]:<19}{table[5]:>8}")

def deactive_scr_table():
    table_print = cursor.execute("SELECT * FROM Student_Cohort_Registration WHERE active = 0").fetchall()
    for table in table_print:
        print()
        print(f"{'Student ID':<12}{'Cohort ID':<11}{'Registration Date':<19}{'Active':>8}")
        print("-" * 50)
        print(f"{table[0]:<12}{table[1]:<11}{table[2]:<19}{table[5]:>8}")

def people_table():
    while True:
        print("""
++++++++++++++++++++
    People Table
++++++++++++++++++++
""")
        options = input("""
(1) - View Active People
(2) - Add Person
(3) - Deactivate Person
(4) - Reactivate Person
(Q) - Go Back To Main Menu
""").lower()
        if options == '1':
            active_people()
        if options == '2':
            create_person()
        if options == '3':
            person_deactivate()
        if options == '4':
            person_reactivate()
        if options == 'q':
            break

def cohort_table():
    while True:
        print("""
++++++++++++++++++++
    Cohort Table
++++++++++++++++++++
""")
        options = input("""
(1) - View Active Cohorts
(2) - Add Cohort
(3) - Deactivate a Cohort
(4) - Reactivate Cohort
(Q) - Go Back To Main Menu
""").lower()

        if options == '1':
            active_cohort()
        if options == '2':
            create_cohort()
        if options == '3':
            cohort_deactivate()
        if options == '4':
            cohort_reactivate()
        if options == 'q':
            break

def courses_table():
    while True:
        print()
        print("""
++++++++++++++++++++++
    Courses Table
++++++++++++++++++++++
""")
        options = input("""
(1) - View Active Courses
(2) - Add Courses
(3) - Deactivate a Course
(4) - Reactivate Courses
(Q) - Go Back To Main Menu
""").lower()

        if options == '1':
            active_course()
        if options == '2':
            create_course()
        if options == '3':
            course_deactivate()
        if options == '4':
            course_reactivate()
        if options == 'q':
            break

def scr_table():
    while True:
        print()
        print("""
+++++++++++++++++++++++++++++++++++++++
   Student Cohort Registration Table
+++++++++++++++++++++++++++++++++++++++
""")
        options = input("""
(1) - View Student Cohort Registration Table
(2) - Register A Student
(3) - Remove A Student
(4) - Complete A Student
(5) - Reactivate Student
(Q) - Go Back To Main Menu
""").lower()

        if options == '1':
            scr_print_table()
        if options == '2':
            student_registration()
        if options == '3':
            remove_student()
        if options == '4':
            student_completion()
        if options == '5':
            student_reactivation()
        if options == 'q':
            break

def main_menu():
    while True:
        menu_input = input("""
+++++++++++++++++++++++++++++++++++++
   Welcome to the Student Database!
+++++++++++++++++++++++++++++++++++++

What would you like to do?

(1) - Enter Persons Table
(2) - Enter Cohort Table
(3) - Enter Courses Table
(4) - Enter Student Cohort Registration Table
(Q) - Exit the program        
\n""").lower()
        if menu_input == '1':
            people_table()
        if menu_input == '2':
            cohort_table()
        if menu_input == '3':
            courses_table() 
        if menu_input == '4':
            scr_table()
        if menu_input == 'q':
            print("Good Bye!")
            break

main_menu()