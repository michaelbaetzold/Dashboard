import tkinter as tk
from tkinter import ttk

import Views.root
from Views import *

import Models.model
from Models.model import *

class App:
    def __init__(self):
        self.window = Views.root.Root()

        self.CreateModelObjects()
        # Run the main event loop
        self.window.mainloop()


    def LoadUserSettings(self):
        #placeholder
        print("test")


    def CreateModelObjects(self):
        # Create an Exam object
        exam1 = Exam()
        exam1.grade = 80
        exam1.exam_type = ExamTypes.WRITTEN_EXAM
        exam1.attempt = 0
        exam1.part_of_final_grade = True

        # Create a Person object
        instructor1 = Person()
        instructor1.name = "John"
        instructor1.last_name = "Doe"
        instructor1.email = "john.doe@example.com"

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
        ]

        # Create a Semester object
        semester1 = Semester()
        semester1.name = "Spring 2024"
        semester1.courses = courses
        semester1.semesterAverage = 85.5

        # Create a DegreeProgram object
        degree_program1 = DegreeProgram()
        degree_program1.name = "Computer Science"
        degree_program1.degree = DegreeTypes.BACHELORS
        degree_program1.semester = [semester1]

        # Create a User object
        user1 = User()
        user1.name = "Alice"
        user1.last_name = "Smith"
        user1.email = "alice.smith@example.com"
        user1.grade_goals = {"CSCI101": 90}
        user1.style = "Visual"
        user1.degree_program = degree_program1

        # Print some attributes of the created courses for verification
        for course in courses:
            print(
                f"Course ID: {course.id}, Name: {course.name}, ECTS: {course.ects}, Exam Type: {course.exam_type.value}")




if __name__ == "__main__":
    app = App()
