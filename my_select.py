from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group
from sqlalchemy import func

engine = create_engine('postgresql://postgres:1111@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    students_with_avg_grade = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
                                     .join(Grade) \
                                     .group_by(Student.id) \
                                     .order_by(func.avg(Grade.grade).desc()) \
                                     .limit(5) \
                                     .all()
    for student, avg_grade in students_with_avg_grade:
        print(f"Student: {student.name}, Average Grade: {avg_grade}")

def select_2(subject_name):
    student_with_highest_avg_grade = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
                                             .join(Grade) \
                                             .join(Subject) \
                                             .filter(Subject.name == subject_name) \
                                             .group_by(Student.id) \
                                             .order_by(func.avg(Grade.grade).desc()) \
                                             .first()
    if student_with_highest_avg_grade:
        student, avg_grade = student_with_highest_avg_grade
        print(f"Student with the highest average grade in {subject_name}: {student.name}, Average Grade: {avg_grade}")
    else:
        print(f"No data found for {subject_name}")

def select_3(subject_name):
    avg_grade_by_group = session.query(Group.name, func.avg(Grade.grade).label('average_grade')) \
                                .join(Student, Group.students) \
                                .join(Grade) \
                                .join(Subject) \
                                .filter(Subject.name == subject_name) \
                                .group_by(Group.name) \
                                .all()
    for group_name, avg_grade in avg_grade_by_group:
        print(f"Group: {group_name}, Average Grade in {subject_name}: {avg_grade}")

def select_4():
    avg_grade_by_subject = session.query(Subject.name, func.avg(Grade.grade).label('average_grade')) \
                                   .join(Grade) \
                                   .group_by(Subject.name) \
                                   .all()
    for subject_name, avg_grade in avg_grade_by_subject:
        print(f"Subject: {subject_name}, Average Grade: {avg_grade}")

def select_5(teacher_name):
    courses_taught = session.query(Subject.name) \
                            .join(Teacher) \
                            .filter(Teacher.name == teacher_name) \
                            .all()
    if courses_taught:
        print(f"Teacher {teacher_name} teaches the following courses:")
        for course in courses_taught:
            print(course[0])
    else:
        print(f"No courses found for teacher {teacher_name}")

def select_6(group_name):
    students_in_group = session.query(Student.name) \
                                .join(Group) \
                                .filter(Group.name == group_name) \
                                .all()
    if students_in_group:
        print(f"Students in group {group_name}:")
        for student in students_in_group:
            print(student[0])
    else:
        print(f"No students found in group {group_name}")

def select_7(group_name, subject_name):
    grades_in_group_subject = session.query(Student.name, Grade.grade) \
                                     .join(Group) \
                                     .join(Grade) \
                                     .join(Subject) \
                                     .filter(Group.name == group_name, Subject.name == subject_name) \
                                     .all()
    if grades_in_group_subject:
        print(f"Grades in group {group_name} for subject {subject_name}:")
        for student, grade in grades_in_group_subject:
            print(f"Student: {student}, Grade: {grade}")
    else:
        print(f"No grades found in group {group_name} for subject {subject_name}")
        
def select_8(teacher_name):
    avg_grade_by_teacher = session.query(func.avg(Grade.grade).label('average_grade')) \
                                   .join(Subject) \
                                   .join(Teacher) \
                                   .filter(Teacher.name == teacher_name) \
                                   .all()
    if avg_grade_by_teacher:
        print(f"Average grade given by teacher {teacher_name}: {avg_grade_by_teacher[0][0]}")
    else:
        print(f"No grades found for teacher {teacher_name}")

def select_9(student_name):
    courses_taken = session.query(Subject.name) \
                           .join(Grade) \
                           .join(Student) \
                           .filter(Student.name == student_name) \
                           .distinct() \
                           .all()
    if courses_taken:
        print(f"Courses taken by student {student_name}:")
        for course in courses_taken:
            print(course[0])
    else:
        print(f"No courses found for student {student_name}")

def select_10(student_name, teacher_name):
    courses_taken_with_teacher = session.query(Subject.name) \
                                        .join(Grade) \
                                        .join(Student) \
                                        .join(Teacher) \
                                        .filter(Student.name == student_name, Teacher.name == teacher_name) \
                                        .distinct() \
                                        .all()
    if courses_taken_with_teacher:
        print(f"Courses taken by student {student_name} with teacher {teacher_name}:")
        for course in courses_taken_with_teacher:
            print(course[0])
    else:
        print(f"No courses found for student {student_name} with teacher {teacher_name}")

if __name__ == "__main__":
    select_1()
    print()
    select_2('Mathematics')
    print()
    select_3('Biology')
    print()
    select_4()
    print()
    select_5('John Smith')
    print()
    select_6('Group A')
    print()
    select_7('Group B', 'Physics')
    print()
    select_8('Jane Doe')
    print()
    select_9('Marvin Hogan')
    print()
    select_10('Nicole Russell', 'Jane Doe')

