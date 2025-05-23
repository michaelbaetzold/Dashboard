import tkinter as tk
from tkinter import ttk
from models import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard")
        self.geometry("1100x600")
        self.minsize(1100, 600)

        # Configure the style for the entire application
        self.style = ttk.Style(self)
        self.style.configure("Header.Label", font=("Arial", 18))
        self.style.configure("Data.Label", font=("Arial", 12, "italic"))

        # Set debug styles
        if False:
            self.style.configure("Overview.TFrame", background="blue")
            self.style.configure("Treeview.TFrame", background="green")
            self.style.configure("TFrame", background="orange")


class View:
    central_frame = ttk.Frame

    def __init__(self):
        self.root = Root()
        self.views = {}

        self._add_view(CourseView, "course")
        self._add_view(DegreeView, "degree")
        self._add_view(SemesterView, "semester")

        self.left_frame = SemesterOverView(master=self.root, style="Treeview.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1, minsize=400)
        self.root.grid_rowconfigure(0, weight=1, pad=10)

    def _add_view(self, Frame, view_name):
        self.views[view_name] = Frame(self.root)
        self.views[view_name].grid(row=0, column=1, sticky="nsew", padx=(10, 10))

    def switch(self, view_name):
        self.central_frame = self.views[view_name]
        self.central_frame.tkraise()

    def start_mainloop(self):
        self.root.mainloop()


class DegreeView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure grid to expand label and progress bars to fill entire frame
        self.grid_rowconfigure(0, weight=6)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=2)
        self.grid_columnconfigure(0, weight=1)

        self.degree_name_var = tk.StringVar()

        self.label = ttk.Label(self, textvariable=self.degree_name_var, font=("Arial", 24))
        self.label.grid(row=0, column=0, sticky="nsew")

        self.label_progress = ttk.Label(self, text="Studienfortschritt", style="Header.Label")
        self.label_progress.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.label_exams = ttk.Label(self, text="Absolvierte Kurse", style="Header.Label")
        self.label_exams.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.exams_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.exams_bar.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

        self.progress_bar["value"] = 0
        self.exams_bar["value"] = 0

    def update_view_from_model(self, degree: DegreeProgram):
        self.degree_name_var.set(degree.name)
        # Check how far the user is in the degree
        current_date = datetime.now()
        total_duration = (degree.end_date - degree.start_date).days
        current_duration = (current_date - degree.start_date).days
        progress_percent = (current_duration / total_duration) * 100
        self.progress_bar["value"] = progress_percent

        # Check the amount of ects the user gathered
        ects_sum = 0
        total_sum = 0
        for semester in degree.semesters:
            for course in semester.courses:
                total_sum += course.ects
                if 0 < course.exam.grade < 4:
                    ects_sum += course.ects
        self.exams_bar["value"] = (ects_sum/total_sum) * 100


class SemesterOverView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header = ttk.Label(master=self, text="Studienübersicht", style="Header.Label")
        self.header.pack(side="top", pady=5)

        self.treeview = SemesterTreeview(self, columns=("average", "object_type"), show="tree")
        self.treeview["displaycolumns"] = ("average")
        self.treeview.column("#1", width=10)
        self.treeview.pack(fill="both", expand=True)



class SemesterTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__grade_table_list = list()

    def update_grade_list(self, grade_table_list):
        self.__grade_table_list = grade_table_list
        for entry in self.__grade_table_list:
            self.tag_configure(entry["color"], background=entry["color"])

    def add_semester_node(self, semester_name: str, item_id: str):
        current_index = self.index(item_id)
        semester_node = self.insert(
            "root_node",
            current_index,
            text=semester_name,
            values=("0.00", "semester"))

        self.insert(
            semester_node,
            "end",
            text="Kurs hinzufügen",
            values=("", "add_course"))

    def get_id_from_name(self, item_name: str):
        children = self.get_children("root_node")
        for child in children:
            if self.item(child)["text"] == item_name:
                return child
            courses = self.get_children(child)
            for course in courses:
                if self.item(course)["text"] == item_name:
                    return course
        print("Name nicht gefunden")


    def get_focussed_indices(self):
        node = self.focus()
        parent = self.parent(node)
        return self.index(parent), self.index(node)


    def add_course_node(self, item_id: str, course_name:str):
        current_index = self.index(item_id)
        semester_node = self.parent(item_id)
        self.insert(
            semester_node,
            current_index,
            text=course_name,
            values=("0.00", "course"))
        return self.item(semester_node)["text"]

    def insert(self, parent, index, *args, **kwargs):
        result = super().insert(parent, index, *args, **kwargs)

        # Set the color based on the grade_table_list
        if "values" in kwargs:
            grade = kwargs["values"][0]
            if not self.__is_float(grade):
                return result
            color = self.__get_grade_color(float(grade))
            self.item(result, tags=color)
        return result

    @staticmethod
    def __is_float(variable):
        try:
            float(variable)
            return True
        except ValueError:
            return False

    def __get_grade_color(self, grade: float):
        current_color = "white"
        if grade <= 0.00:
            return current_color

        for entry in self.__grade_table_list:
            if grade <= entry["grade"]:
                current_color = entry["color"]

        return current_color


class CourseView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Frames
        self.course_name_frame = ttk.Frame(self, style="Test.TFrame")
        self.course_id_frame = ttk.Frame(self)
        self.exam_details_frame = ttk.Frame(self)
        self.grade_frame = ttk.Frame(self)
        self.attempt_frame = ttk.Frame(self)
        self.part_of_final_grade_frame = ttk.Frame(self)
        self.ects_frame = ttk.Frame(self)

        # Entry fields
        self.course_name_var = tk.StringVar()
        self.course_id_var = tk.StringVar()
        self.exam_details_var = tk.StringVar()
        self.grade_var = tk.DoubleVar()
        self.attempt_var = tk.IntVar()
        self.part_of_final_grade_var = tk.BooleanVar()
        self.ects_var = tk.IntVar()

        # Course name
        self.course_name_label = ttk.Label(self.course_name_frame, text="Kurs Name")
        self.course_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.course_name_entry = ttk.Entry(self.course_name_frame, textvariable=self.course_name_var)
        self.course_name_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=4)

        # Course ID
        self.course_id_label = ttk.Label(self.course_id_frame, text="Kurs ID")
        self.course_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.course_id_entry = ttk.Entry(self.course_id_frame, textvariable=self.course_id_var)
        self.course_id_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=3)

        # Exam details
        self.exam_details_label = ttk.Label(self.exam_details_frame, text="Prüfungsdetails")
        self.exam_details_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.exam_details_entry = ttk.Entry(self.exam_details_frame, textvariable=self.exam_details_var)
        self.exam_details_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=3)

        # Grade
        self.grade_label = ttk.Label(self.grade_frame, text="Note")
        self.grade_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.grade_entry = ttk.Entry(self.grade_frame, textvariable=self.grade_var)
        self.grade_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=3)

        # Attempt
        self.attempt_label = ttk.Label(self.attempt_frame, text="Versuch")
        self.attempt_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.attempt_entry = ttk.Entry(self.attempt_frame, textvariable=self.attempt_var)
        self.attempt_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=3)

        # Part of final grade
        self.part_of_final_grade_check = ttk.Checkbutton(self.part_of_final_grade_frame,
                                                         text="Teil der Abschlussnote",
                                                         variable=self.part_of_final_grade_var)
        self.part_of_final_grade_check.grid(row=0, column=0, sticky="w", padx=10, pady=5, columnspan=3)

        # ECTS
        self.ects_label = ttk.Label(self.ects_frame, text="ECTS")
        self.ects_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.ects_entry = ttk.Entry(self.ects_frame, textvariable=self.ects_var)
        self.ects_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5, columnspan=3)

        # Buttons
        self.button_del = ttk.Button(self, text="Kurs löschen")
        self.button_del.grid(row=8, column=0, sticky="se", padx=100, pady=10)
        self.button = ttk.Button(self, text="Speichern")
        self.button.grid(row=8, column=0, sticky="se", padx=10, pady=10)

        # Place frames in grid
        self.course_name_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.course_id_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.exam_details_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.grade_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.attempt_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        self.part_of_final_grade_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        self.ects_frame.grid(row=6, column=0, sticky="ew", padx=10, pady=5)

        # Configure row and column weights
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_view_from_model(self, course: Course):
        self.course_name_var.set(course.name)
        self.course_id_var.set(course.course_id)
        self.exam_details_var.set(course.exam.exam_type.value)
        self.grade_var.set(course.exam.grade)
        self.attempt_var.set(course.exam.attempt)
        self.part_of_final_grade_var.set(course.exam.part_of_final_grade)
        self.ects_var.set(course.ects)


class SemesterView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.semester_name_var = tk.StringVar()
        self.semester_name_var.set("Semester 1")

        self.header_label = ttk.Label(self, textvariable=self.semester_name_var, font=("Arial", 24, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.header_label = ttk.Label(self, text="ausstehende Kurse", font=("Arial", 16))
        self.header_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.treeview = ttk.Treeview(self, columns=("Course ID", "Course Name"), show="headings")
        self.treeview.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.treeview.heading("Course ID", text="Kurs ID")
        self.treeview.heading("Course Name", text="Kurs Name")

        self.button_del = ttk.Button(self, text="Semester löschen")
        self.button_del.grid(row=3, column=0, sticky="se", padx=10, pady=10)

    def update_view_from_model(self, semester: Semester):
        self.semester_name_var.set(semester.name)
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for course in semester.courses:
            if course.exam.grade <= 0:
                self.treeview.insert("", "end", values=(course.course_id, course.name))
