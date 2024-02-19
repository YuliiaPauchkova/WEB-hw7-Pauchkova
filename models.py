from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:1111@localhost:5432/postgres')

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    grades = relationship('Grade', backref='student')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship('Student', backref='group')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship('Subject', backref='teacher')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    grades = relationship('Grade', backref='subject')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Float)
    date_received = Column(Date)

# Створення таблиць у базі даних
Base.metadata.create_all(engine)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Закриття сесії
session.close()