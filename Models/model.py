from enum import Enum
from datetime import datetime

import random


# <editor-fold desc="Enums">
class ExamTypes(Enum):
    WRITTEN_EXAM = "Klausur"
    TECHNICAL_PRESENTATION = "Fachpräsentation"
    ADVANCED_WORKBOOK = "Advanced Workbook"
    PORTFOLIO = "Portfolio"
    CASE_STUDY = "Fallstudie"
    PROJECT_REPORT = "Projektbericht"
    PROJECT_PRESENTATION = "Projektpräsentation"
    SEMINAR_PAPER = "Seminararbeit"
    ACADEMIC_PAPER = "Hausarbeit"
    BACHELOR_THESIS = "Bachelorarbeit"
    UNKNOWN = "Unbekannt"


class DegreeTypes(Enum):
    BACHELORS = 1
    MASTERS = 2
    DOCTORATE = 3


#</editor-fold>


# <editor-fold desc="Classes">

class Exam:
    def __init__(self, grade: float, exam_type: ExamTypes, attempt: int, part_of_final_grade: bool):
        self.grade = grade
        self.exam_type = exam_type
        self.attempt = attempt
        self.part_of_final_grade = part_of_final_grade

    def to_json(self):
        return {
            "grade": self.grade,
            "exam_type": self.exam_type.value,
            "attempt": self.attempt,
            "part_of_final_grade": self.part_of_final_grade
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

class Course:
    def __init__(self, course_id: str, name: str, ects: int, exam: Exam):
        self.course_id = course_id
        self.name = name
        self.ects = ects
        self.exam = exam

    def to_json(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "ects": self.ects,
            "exam": self.exam.to_json()
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["course_id"], json_data["name"], json_data["ects"], Exam.from_json(json_data["exam"]))

class Semester:
    def __init__(self, name: str, courses: [Course], semester_average: float):
        self.name = name
        self.courses = courses
        self.semester_average = semester_average

    def to_json(self):
        return {
            "name": self.name,
            "courses": [course.to_json() for course in self.courses],
            "semester_average": self.semester_average
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["name"], [Course.from_json(course_data) for course_data in json_data["courses"]], json_data["semester_average"])

class DegreeProgram:
    def __init__(self, name: str, degree: DegreeTypes, semesters: [Semester], start_date: datetime, end_date: datetime):
        self.name = name
        self.degree = degree
        self.semesters = semesters
        self.start_date = start_date
        self.end_date = end_date

    def to_json(self):
        return {
            "name": self.name,
            "degree": self.degree.value,
            "semesters": [semester.to_json() for semester in self.semesters],
            "start_date": self.start_date.strftime("%d %B %Y"),
            "end_date": self.end_date.strftime("%d %B %Y")
        }

    @classmethod
    def from_json(cls, json_data):
        semesters = [Semester.from_json(semester_data) for semester_data in json_data["semesters"]]
        start_date = datetime.strptime(json_data["start_date"], "%d %B %Y")
        end_date = datetime.strptime(json_data["end_date"], "%d %B %Y")
        return cls(json_data["name"], DegreeTypes(json_data["degree"]), semesters, start_date, end_date)

class User:
    def __init__(self, grade_goals: dict, style: str, degree_program: DegreeProgram):
        self.grade_goals = grade_goals
        self.style = style
        self.degree_program = degree_program

    def to_json(self):
        return {
            "grade_goals": self.grade_goals,
            "style": self.style,
            "degree_program": self.degree_program.to_json()
        }

    @classmethod
    def from_json(cls, json_data):
        degree_program = DegreeProgram.from_json(json_data["degree_program"])
        return cls(json_data["grade_goals"], json_data["style"], degree_program)
# class Exam:
#     grade = float
#     exam_type = ExamTypes
#     attempt = int
#     part_of_final_grade = bool
#
#
# class Course:
#     course_id = str
#     exam = Exam
#     name = str
#     ects = int
#
#     def __init__(self, course_id: str, name: str, ects: int, exam_type: ExamTypes):
#         super().__init__()
#         self.course_id = course_id
#         self.name = name
#         self.ects = ects
#         self.exam = Exam()
#         self.exam.exam_type = exam_type
#         self.exam.grade = 0.00 #round(random.triangular(1.00, 6.00, 1.3), 2)
#         self.exam.part_of_final_grade = True
#         self.exam.attempt = 1
#
#
# class Semester:
#     name = str
#     courses = []
#     semesterAverage = float
#
#     def __init__(self, name: str, courses: [Course]):
#         super().__init__()
#         self.name = name
#         self.courses = courses
#         self.semester_average = 0.00
#
#
# class DegreeProgram:
#     name = str
#     degree = DegreeTypes
#     semesters = []
#     start_date = datetime.strptime("28 November 2023", "%d %B %Y")
#     end_date = datetime.strptime("28 November 2027", "%d %B %Y")
#
#
# class User:
#     grade_goals = {}
#     style = str
#     degree_program = DegreeProgram

#</editor-fold>

class Model:
    def __init__(self):
        self.user = self.load_model_objects()

    def get_degree_program(self):
        return self.user.degree_program

    def get_course_from_name(self, name):
        for semester in self.user.degree_program.semesters:
            for course in semester.courses:
                if course.name == name:
                    return course
        return None

    def get_semester_from_name(self, name):
        for semester in self.user.degree_program.semesters:
            if semester.name == name:
                return semester
        return None

    def load_model_objects(self) -> User:
        # Create an Exam object
        exam1 = Exam()
        exam1.grade = 80
        exam1.exam_type = ExamTypes.WRITTEN_EXAM
        exam1.attempt = 0
        exam1.part_of_final_grade = True

        # Create a Course object
        courses = [
            Course("DLBDSEAIS01_D", "Artificial Intelligence", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBWIRITT01", "Einführung in das wissenschaftliche Arbeiten für IT und Technik", 5,
                   ExamTypes.ADVANCED_WORKBOOK),
            Course("DLBDSIPWP01_D", "Einführung in die Programmierung mit Python", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBBIMD01", "Mathematics: Analysis", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBKA01", "Kollaboratives Arbeiten", 5, ExamTypes.TECHNICAL_PRESENTATION),
            Course("DLBDSSPDS01_D", "Statistics - Probability and Descriptive Statistics", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBDSOOFPP01_D", "Objektorientierte und funktionale Programmierung mit Python", 5,
                   ExamTypes.PORTFOLIO),
            Course("DLBBIM01", "Mathematik: Lineare Algebra", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBIHK01", "Interkulturelle und ethische Handlungskompetenz", 5, ExamTypes.CASE_STUDY),
            Course("DLBDSSIS01_D", "Statistik - Schließende Statistik", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBDSCC01_D", "Cloud Computing", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBSEPCP01_D", "Cloud Programming", 5, ExamTypes.PORTFOLIO),
            Course("DLBDSMLSL01_D", "Maschinelles Lernen - Supervised Learning", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBDSMLUSL01_D", "Maschinelles Lernen - Unsupervised Learning und Feature Engineering", 5,
                   ExamTypes.CASE_STUDY),
            Course("DLBDSNNDL01_D", "Neuronale Netze und Deep Learning", 5, ExamTypes.TECHNICAL_PRESENTATION),
            Course("DLBAIICV01_D", "Einführung in Computer Vision", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBAIPCV01_D", "Projekt: Computer Vision", 5, ExamTypes.PROJECT_REPORT),
            Course("DLBAIIRL01_D", "Einführung in das Reinforcement Learning", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBAIINLP01_D", "Einführung in NLP", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBAIPNLP01_D", "Projekt: NLP", 5, ExamTypes.PROJECT_REPORT),
            Course("DLBISIC01", "Einführung in Datenschutz und IT-Sicherheit", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBDSDSSE01_D", "Data Science Software Engineering", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBDSMTP01_D", "Projekt: Vom Modell zum Produktvertrieb", 5, ExamTypes.PROJECT_REPORT),
            Course("DLBDSSECDS01_D", "Seminar: Ethische Fragen der Data Science", 5, ExamTypes.SEMINAR_PAPER),
            Course("DLBMIUEX01", "User Experience", 5, ExamTypes.WRITTEN_EXAM),
            Course("DLBAIPEAI01_D", "Projekt: Edge AI", 5, ExamTypes.PROJECT_REPORT),
            Course("DLBROIR01_D", "Einführung in die Robotik", 5, ExamTypes.ACADEMIC_PAPER),
            Course("DLBDBAPM01", "Agiles Projektmanagement", 5, ExamTypes.PROJECT_REPORT),
            Course("", "Wahlpflichtmodul A", 10, ExamTypes.UNKNOWN),
            Course("", "Wahlpflichtmodul B", 10, ExamTypes.UNKNOWN),
            Course("", "Wahlpflichtmodul C", 10, ExamTypes.UNKNOWN),
            Course("BBAK01, BBAK02", "Bachelorarbeit", 10, ExamTypes.BACHELOR_THESIS)
        ]

        # Create a Semester object
        semesters = [
            Semester("Semester 1", courses[:5]),
            Semester("Semester 2", courses[5:9]),
            Semester("Semester 3", courses[9:14]),
            Semester("Semester 4", courses[14:18]),
            Semester("Semester 5", courses[18:23]),
            Semester("Semester 6", courses[23:27]),
            Semester("Semester 8", courses[27:30]),
            Semester("Semester 6", courses[30:])
        ]

        # Create a DegreeProgram object
        degree_program1 = DegreeProgram()
        degree_program1.name = "Angewandte Künstliche Intelligenz"
        degree_program1.degree = DegreeTypes.BACHELORS
        degree_program1.semesters = semesters

        # Create a User object
        user = User()
        user.grade_goals = {}
        user.style = "Clam"
        user.degree_program = degree_program1

        return user
