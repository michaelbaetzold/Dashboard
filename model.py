from enum import Enum


class Person:
    name = str
    email = str


class User(Person):
    gradeGoals = {}


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



