from enum import Enum


class Observable:
    def __init__(self):
        self._event_listeners = {}

    def add_event_listener(self, event, fn):
        try:
            self._event_listeners[event].append(fn)
        except KeyError:
            self._event_listeners[event] = [fn]

        return lambda: self._event_listeners[event].remove(fn)

    def trigger_event(self, event):
        if event not in self._event_listeners.keys():
            return

        for func in self._event_listeners[event]:
            func(self)


# <editor-fold desc="Enums">
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


# <editor-fold desc="Classes">
class Exam(Observable):
    grade = float
    exam_type = ExamTypes
    attempt = int
    part_of_final_grade = bool


class Person(Observable):
    name = str
    last_name = str
    email = str


class Course(Observable):
    id = str
    exam = Exam
    instructor = Person
    name = str
    ects = int

    def __init__(self, id, name, ects, exam_type):
        super().__init__()
        self.id = id
        self.name = name
        self.ects = ects
        self.exam_type = exam_type


class Semester(Observable):
    name = str
    courses = []
    semesterAverage = float


class DegreeProgram(Observable):
    name = str
    degree = DegreeTypes
    semester = []


class User(Person):
    grade_goals = {}
    style = str
    degree_program = DegreeProgram

#</editor-fold>