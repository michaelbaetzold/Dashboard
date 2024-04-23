from enum import Enum
from datetime import datetime
import json


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

    @classmethod
    def get_exam_type(cls, name):
        for exam in ExamTypes:
            if exam.value == name:
                return exam


class DegreeTypes(Enum):
    BACHELORS = 1
    MASTERS = 2
    DOCTORATE = 3


# </editor-fold>


# <editor-fold desc="Model Classes">
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
        # Deserialize enum
        exam_type_str = json_data.get("exam_type")
        exam_type = ExamTypes(exam_type_str)
        return cls(
            json_data["grade"],
            exam_type,
            json_data["attempt"],
            json_data["part_of_final_grade"]
        )


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
        self.semester_average = self.update_semester_average()

    def update_semester_average(self):
        grades = [
            course.exam.grade
            for course in self.courses
            if course.exam.part_of_final_grade and float(course.exam.grade) > 0.0
        ]
        self.semester_average = sum(grades) / len(grades) if grades else 0.0
        return self.semester_average

    def to_json(self):
        return {
            "name": self.name,
            "courses": [course.to_json() for course in self.courses],
            "semester_average": self.semester_average
        }

    @classmethod
    def from_json(cls, json_data):
        courses = [Course.from_json(course_data) for course_data in json_data["courses"]]
        semester_average = 0.0
        return cls(json_data["name"], courses, semester_average)


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
    def __init__(self, grade_goals: list, style: str, degree_program: DegreeProgram):
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


# </editor-fold>


class Model:
    FILE_PATH = "data.json"
    user = User

    def __init__(self):
        self.load_data_from_json()

    def load_data_from_json(self):
        try:
            with open(self.FILE_PATH, "r") as file:
                json_string = file.read()
            self.user = User.from_json(json.loads(json_string))
        except FileNotFoundError:
            self.user = self.load_model_objects()

    def save_data_to_json(self):
        json_string = self.user.to_json()
        json_data = json.dumps(json_string, indent=4)

        # Write the JSON data to a file
        with open(self.FILE_PATH, "w") as file:
            file.write(json_data)

    def get_degree_program(self):
        return self.user.degree_program

    def get_course_from_name(self, name):
        for semester in self.user.degree_program.semesters:
            for course in semester.courses:
                if course.name == name:
                    return course
        return None # TODO Error when inserting new course and saving name

    def get_semester_from_name(self, name):
        for semester in self.user.degree_program.semesters:
            if semester.name == name:
                return semester
        return None

    def get_next_semester_name(self):
        current_semester_number = len(self.user.degree_program.semesters)
        return f"Semester {current_semester_number + 1}"

    def update_course_model_from_view(self, new_course: Course):
        for semester in self.user.degree_program.semesters:
            for index, course in enumerate(semester.courses):
                if course.name == new_course.name or course.course_id == new_course.course_id:
                    semester.courses[index] = new_course
                    semester.update_semester_average()
                    return
        print("unsuccessful update")

    def load_model_objects(self) -> User:  # Keep as backup
        exams = [
            Exam(1.2, ExamTypes.WRITTEN_EXAM, 1, True),  # Artificial Intelligence
            Exam(2.0, ExamTypes.ADVANCED_WORKBOOK, 1, True),
            # Einführung in das wissenschaftliche Arbeiten für IT und Technik
            Exam(1.0, ExamTypes.WRITTEN_EXAM, 1, True),  # Einführung in die Programmierung mit Python
            Exam(2.1, ExamTypes.WRITTEN_EXAM, 1, True),  # Mathematics: Analysis
            Exam(1.0, ExamTypes.TECHNICAL_PRESENTATION, 1, False),  # Kollaboratives Arbeiten
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Statistics - Probability and Descriptive Statistics
            Exam(0, ExamTypes.PORTFOLIO, 1, True),  # Objektorientierte und funktionale Programmierung mit Python
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Mathematik: Lineare Algebra
            Exam(0, ExamTypes.CASE_STUDY, 1, True),  # Interkulturelle und ethische Handlungskompetenz
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Statistik - Schließende Statistik
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Cloud Computing
            Exam(0, ExamTypes.PORTFOLIO, 1, True),  # Cloud Programming
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Maschinelles Lernen - Supervised Learning
            Exam(0, ExamTypes.CASE_STUDY, 1, True),
            # Maschinelles Lernen - Unsupervised Learning und Feature Engineering
            Exam(0, ExamTypes.TECHNICAL_PRESENTATION, 1, True),  # Neuronale Netze und Deep Learning
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Einführung in Computer Vision
            Exam(0, ExamTypes.PROJECT_REPORT, 1, True),  # Projekt: Computer Vision
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Einführung in das Reinforcement Learning
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Einführung in NLP
            Exam(0, ExamTypes.PROJECT_REPORT, 1, True),  # Projekt: NLP
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Einführung in Datenschutz und IT-Sicherheit
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # Data Science Software Engineering
            Exam(0, ExamTypes.PROJECT_REPORT, 1, True),  # Projekt: Vom Modell zum Produktvertrieb
            Exam(0, ExamTypes.SEMINAR_PAPER, 1, True),  # Seminar: Ethische Fragen der Data Science
            Exam(0, ExamTypes.WRITTEN_EXAM, 1, True),  # User Experience
            Exam(0, ExamTypes.PROJECT_REPORT, 1, True),  # Projekt: Edge AI
            Exam(0, ExamTypes.ACADEMIC_PAPER, 1, True),  # Einführung in die Robotik
            Exam(0, ExamTypes.PROJECT_REPORT, 1, True),  # Agiles Projektmanagement
            Exam(0, ExamTypes.UNKNOWN, 1, True),  # Wahlpflichtmodul A
            Exam(0, ExamTypes.UNKNOWN, 1, True),  # Wahlpflichtmodul B
            Exam(0, ExamTypes.UNKNOWN, 1, True),  # Wahlpflichtmodul C
            Exam(0, ExamTypes.BACHELOR_THESIS, 1, True)  # Bachelorarbeit
        ]

        courses = [
            Course("DLBDSEAIS01_D", "Artificial Intelligence", 5, exams[0]),
            Course("DLBWIRITT01", "Einführung in das wissenschaftliche Arbeiten für IT und Technik", 5, exams[1]),
            Course("DLBDSIPWP01_D", "Einführung in die Programmierung mit Python", 5, exams[2]),
            Course("DLBBIMD01", "Mathematics: Analysis", 5, exams[3]),
            Course("DLBKA01", "Kollaboratives Arbeiten", 5, exams[4]),
            Course("DLBDSSPDS01_D", "Statistics - Probability and Descriptive Statistics", 5, exams[5]),
            Course("DLBDSOOFPP01_D", "Objektorientierte und funktionale Programmierung mit Python", 5, exams[6]),
            Course("DLBBIM01", "Mathematik: Lineare Algebra", 5, exams[7]),
            Course("DLBIHK01", "Interkulturelle und ethische Handlungskompetenz", 5, exams[8]),
            Course("DLBDSSIS01_D", "Statistik - Schließende Statistik", 5, exams[9]),
            Course("DLBDSCC01_D", "Cloud Computing", 5, exams[10]),
            Course("DLBSEPCP01_D", "Cloud Programming", 5, exams[11]),
            Course("DLBDSMLSL01_D", "Maschinelles Lernen - Supervised Learning", 5, exams[12]),
            Course("DLBDSMLUSL01_D", "Maschinelles Lernen - Unsupervised Learning und Feature Engineering", 5,
                   exams[13]),
            Course("DLBDSNNDL01_D", "Neuronale Netze und Deep Learning", 5, exams[14]),
            Course("DLBAIICV01_D", "Einführung in Computer Vision", 5, exams[15]),
            Course("DLBAIPCV01_D", "Projekt: Computer Vision", 5, exams[16]),
            Course("DLBAIIRL01_D", "Einführung in das Reinforcement Learning", 5, exams[17]),
            Course("DLBAIINLP01_D", "Einführung in NLP", 5, exams[18]),
            Course("DLBAIPNLP01_D", "Projekt: NLP", 5, exams[19]),
            Course("DLBISIC01", "Einführung in Datenschutz und IT-Sicherheit", 5, exams[20]),
            Course("DLBDSDSSE01_D", "Data Science Software Engineering", 5, exams[21]),
            Course("DLBDSMTP01_D", "Projekt: Vom Modell zum Produktvertrieb", 5, exams[22]),
            Course("DLBDSSECDS01_D", "Seminar: Ethische Fragen der Data Science", 5, exams[23]),
            Course("DLBMIUEX01", "User Experience", 5, exams[24]),
            Course("DLBAIPEAI01_D", "Projekt: Edge AI", 5, exams[25]),
            Course("DLBROIR01_D", "Einführung in die Robotik", 5, exams[26]),
            Course("DLBDBAPM01", "Agiles Projektmanagement", 5, exams[27]),
            Course("", "Wahlpflichtmodul A", 10, exams[28]),
            Course("", "Wahlpflichtmodul B", 10, exams[29]),
            Course("", "Wahlpflichtmodul C", 10, exams[30]),
            Course("BBAK01, BBAK02", "Bachelorarbeit", 10, exams[31])
        ]

        semesters = [
            Semester("Semester 1", courses[:5], 0.0),
            Semester("Semester 2", courses[5:9], 0.0),
            Semester("Semester 3", courses[9:14], 0.0),
            Semester("Semester 4", courses[14:18], 0.0),
            Semester("Semester 5", courses[18:23], 0.0),
            Semester("Semester 6", courses[23:27], 0.0),
            Semester("Semester 7", courses[27:30], 0.0),
            Semester("Semester 8", courses[30:], 0.0)
        ]

        degree_program1 = DegreeProgram("Angewandte Künstliche Intelligenz", DegreeTypes.BACHELORS, semesters,
                                        datetime.strptime("28 November 2023", "%d %B %Y"),
                                        datetime.strptime("28 November 2027", "%d %B %Y"))

        user = User(
            [{"grade": 6.0, "color": "#FF2C2C"},
             {"grade": 2.5, "color": "orange"},
             {"grade": 1.7, "color": "yellow"},
             {"grade": 1.3, "color": "#39E75F"}],
            "Clam",
            degree_program=degree_program1
        )

        return user
