from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy.exc import IntegrityError
from random import randint

# Підключення до бази даних
engine = create_engine('postgresql://postgres:1111@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація Faker
fake = Faker()

# Функція для створення випадкових даних для студентів
def create_students(num_students):
    for _ in range(num_students):
        name = fake.name()
        group_id = randint(1, 3)
        student = Student(name=name, group_id=group_id)
        session.add(student)

# Функція для створення випадкових даних для груп
def create_groups():
    groups = ['Group A', 'Group B', 'Group C']
    for group_name in groups:
        group = Group(name=group_name)
        session.add(group)

# Функція для створення випадкових даних для викладачів
def create_teachers(num_teachers):
    for _ in range(num_teachers):
        name = fake.name()
        teacher = Teacher(name=name)
        session.add(teacher)

# Функція для створення випадкових даних для предметів
def create_subjects(num_subjects):
    subjects = [
        'Mathematics', 'Physics', 'Chemistry', 'Biology', 'History',
        'Geography', 'Literature', 'English', 'Computer Science', 'Art'
    ]
    for i in range(num_subjects):
        subject = Subject(name=subjects[i % len(subjects)], teacher_id=randint(1, 3))
        session.add(subject)
    session.commit()

# Функція для створення випадкових даних для оцінок
def create_grades(num_grades):
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for _ in range(num_grades):
        student = fake.random_element(students)
        subject = fake.random_element(subjects)
        grade = fake.random_int(min=1, max=10)
        date_received = fake.date_this_year()
        new_grade = Grade(student_id=student.id, subject_id=subject.id, grade=grade, date_received=date_received)
        session.add(new_grade)

# Заповнення бази даних випадковими даними
try:
    create_groups()
    create_teachers(5)
    create_subjects(8)
    create_students(40)
    create_grades(200)
    session.commit()
    print("Дані успішно додані до бази даних.")
except IntegrityError:
    session.rollback()
    print("Помилка: Дані вже існують або порушені обмеження унікальності.")
finally:
    session.close()
