from enum import Enum


#<editor-fold desc="Enums">
class ExamTypes(Enum):
    WRITTEN_EXAM = 1
    TECHNICAL_PRESENTATION = 2
    ADVANCED_WORKBOOK = 3
    PORTFOLIO = 4
    CASE_STUDY = 5
    PROJECT_REPORT = 6
    PROJECT_PRESENTATION = 7
    SEMINAR_PAPER = 8
    ACADEMIC_PAPER = 9
    BACHELOR_THESIS = 10


class DegreeTypes(Enum):
    BACHELORS = 1
    MASTERS = 2
    DOCTORATE = 3

#</editor-fold>


#<editor-fold desc="Classes">
class Exam:
    grade = float
    exam_type = ExamTypes
    attempt = int
    part_of_final_grade = bool


class Person:
    name = str
    last_name = str
    email = str


class Course:
    id = str
    exam = Exam
    instructor = Person
    name = str
    ects = int


class Semester:
    name = str
    courses = []
    semesterAverage = float


class DegreeProgram:
    name = str
    degree = DegreeTypes
    semester = []


class User(Person):
    grade_goals = {}
    style = str
    degree_program = DegreeProgram

#</editor-fold>