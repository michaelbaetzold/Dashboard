import tkinter as tk
from operator import xor
from tkinter import ttk

from Models.model import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard")
        self.geometry("1100x600")
        self.minsize(1100, 600)

        # Configure the style for the entire application
        self.style = ttk.Style(self)
        self.style.configure('Overview.TFrame', background="blue")
        self.style.configure('Treeview.TFrame', background="green")
        self.style.configure('TFrame', background="orange")


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

        self.label_progress = ttk.Label(self, text="Studienfortschritt")
        self.label_progress.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.label_exams = ttk.Label(self, text="Absolvierte Kurse")
        self.label_exams.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.exams_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.exams_bar.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

        # Set initial values for progress bars (if needed)
        self.progress_bar["value"] = 50  # Example value
        self.exams_bar["value"] = 30  # Example value

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

        # Create Header
        self.header = ttk.Label(master=self, text="Studienübersicht")
        self.header.pack(side="top", pady=5)

        # Create a Treeview widget in the left frame
        self.treeview = SemesterTreeview(self, columns=("average", "object_type"), show="tree")
        self.treeview["displaycolumns"] = ("average")
        #self.treeview.column("#0", width=350)
        self.treeview.column("#1", width=10)
        self.treeview.pack(fill="both", expand=True)

    def create_tree_view_from_model(self, degree_program: DegreeProgram):

        self.treeview.insert("", "end", "root_node", text=degree_program.name, values=("", "degree"))

        for semester_num, semester in enumerate(degree_program.semesters, start=1):
            # Insert the semester node under the root node
            semester_node = self.treeview.insert(
                "root_node",
                "end", text=f"Semester {semester_num}",
                values=(semester.semester_average, "semester"))

            # Iterate over each course in the semester
            for course in semester.courses:
                # Insert the course node under the semester node
                self.treeview.insert(semester_node, "end", text=course.name, values=(course.exam.grade, "course"))


class SemesterTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the color table
        self.__grade_table_list = [
            {"grade": 6.0, "color": "red"},
            {"grade": 4.0, "color": "orange"},
            {"grade": 2.0, "color": "yellow"},
            {"grade": 1.5, "color": "green"}
        ]

        # Create the color tags
        for entry in self.__grade_table_list:
            self.tag_configure(entry["color"], background=entry["color"])

    def insert(self, parent, index, *args, **kwargs):
        # Call the original insert method to perform the insertion
        result = super().insert(parent, index, *args, **kwargs)

        # Set the color based on the grade_table_list
        if 'values' in kwargs:
            grade = kwargs['values'][0]
            if not isinstance(grade, float):
                return result
            color = self.__get_grade_color(grade)
            self.item(result, tags=color)
        return result

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

        # StringVars for entry fields
        self.course_name_var = tk.StringVar()
        self.course_id_var = tk.StringVar()
        self.exam_details_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.attempt_var = tk.IntVar()
        self.part_of_final_grade_var = tk.BooleanVar()

        # Course name entry field
        self.course_name_entry = ttk.Entry(self, textvariable=self.course_name_var)
        self.course_name_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Course ID entry field
        self.course_id_entry = ttk.Entry(self, textvariable=self.course_id_var)
        self.course_id_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # Exam details entry field
        self.exam_details_entry = ttk.Entry(self, textvariable=self.exam_details_var)
        self.exam_details_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Grade entry field
        self.grade_entry = ttk.Entry(self, textvariable=self.grade_var)
        self.grade_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Attempt entry field
        self.attempt_entry = ttk.Entry(self, textvariable=self.attempt_var)
        self.attempt_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

        # Part of final grade checkbox
        self.part_of_final_grade_check = ttk.Checkbutton(self, text="Teil der Abschlussnote",
                                                         variable=self.part_of_final_grade_var)
        self.part_of_final_grade_check.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        # Save button
        self.button = ttk.Button(self, text="Speichern")
        self.button.grid(row=6, column=0, sticky="se", padx=10, pady=10)

        # Configure row and column weights
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_view_from_model(self, course: Course):
        self.course_name_var.set(course.name)
        self.course_id_var.set(course.course_id)
        self.exam_details_var.set(course.exam.exam_type.value)
        self.grade_var.set(course.exam.grade)
        self.attempt_var.set(course.exam.attempt)
        self.part_of_final_grade_var.set(course.exam.part_of_final_grade)


class SemesterView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # StringVars for header labels
        self.semester_name_var = tk.StringVar()
        self.semester_name_var.set("Semester 1")  # Set default semester name

        # Header label with big font
        self.header_label = ttk.Label(self, textvariable=self.semester_name_var, font=("Arial", 24, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)

        # label for treeview
        self.header_label = ttk.Label(self, text="ausstehende Kurse", font=("Arial", 16))
        self.header_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Create a treeview for the table
        self.treeview = ttk.Treeview(self, columns=("Course ID", "Course Name"), show="headings")
        self.treeview.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Define column headings
        self.treeview.heading("Course ID", text="Kurs ID")
        self.treeview.heading("Course Name", text="Kurs Name")

    def update_view_from_model(self, semester: Semester):
        self.semester_name_var.set(semester.name)
        # Clear existing items in the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Loop over semester courses
        for course in semester.courses:
            if course.exam.grade <= 0:
                # Add course ID and name to the treeview
                self.treeview.insert("", "end", values=(course.course_id, course.name))
