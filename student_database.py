import sqlite3

connection = sqlite3.connect('my_student_data.db')
cursor = connection.cursor()

def student_database(cursor):
    with open("student_database_schema.sql") as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
    connection.commit()


student_database(cursor)