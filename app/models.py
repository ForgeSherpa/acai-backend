from sqlalchemy import Column, Date, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

class Lecturer(Base):
    __tablename__ = 'lecturers'

    id = Column(Integer, primary_key=True)
    nidn = Column(Integer, index=True)
    name = Column(String)

    researches = relationship("LecturerResearch", back_populates="lecturer")

class LecturerResearch(Base):
    __tablename__ = 'lecturer_researches'

    id = Column(Integer, primary_key=True) # id dosen
    nidn = Column(Integer, ForeignKey('lecturers.nidn'))
    title = Column(String)
    publication_date = Column(Date)
    publication_type = Column(String, nullable=True)
    publication_detail = Column(String)

    lecturer = relationship("Lecturer", back_populates="researches")

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True) # npm
    name = Column(String)
    faculty = Column(String)
    generation = Column(Integer)
    gpa = Column(Float)
    status = Column(String)
    graduation_year = Column(Integer)
    graduation_semester = Column(Integer)

    activities = relationship("StudentActivity", back_populates="student")

class StudentActivity(Base):
    __tablename__ = 'student_activities'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    bank_id = Column(Integer)
    name = Column(String)
    type = Column(String)
    date = Column(Date)

    student = relationship("Student", back_populates="activities")