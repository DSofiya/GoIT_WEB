import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

# Підключення до бази даних
conn = psycopg2.connect(host="localhost", database="homework", user="postgres", password="1111")
cur = conn.cursor()

# Додавання груп
for _ in range(3):
    group_name = fake.random_element(["Group A", "Group B", "Group C"])
    cur.execute("INSERT INTO groups (name) VALUES (%s)", (group_name,))
    

# Заповнення таблиці викладачів
for _ in range(3):
    teacher_name = fake.name()
    cur.execute("INSERT INTO teachers (fullname) VALUES (%s)", (teacher_name,))

# Заповнення таблиці предметів
for _ in range(5):
    subject_name = fake.catch_phrase()
    teacher_id = random.randint(1, 3)  # вибираємо випадкового викладача
    cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", (subject_name, teacher_id))

# Заповнення таблиці студентів
for _ in range(50):
    student_name = fake.name()
    group_id = random.randint(1, 3)  # вибираємо випадкову групу
    cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s)", (student_name, group_id))

# Заповнення таблиці оцінок
for student_id in range(1, 51):
    for subject_id in range(1, 6):
        grade = random.randint(0, 100)
        grade_date = fake.date_this_decade()
        cur.execute("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                    (student_id, subject_id, grade, grade_date))

try:
    # Збереження змін
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закриття підключення
    cur.close()
    conn.close()