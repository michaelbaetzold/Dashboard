import tkinter as tk
from tkinter import ttk

from Models.model import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        #self = tk.Tk()
        self.title("Dashboard")
        self.geometry("1000x600")
        self.minsize(500, 300)

        # Configure the style for the entire application
        self.style = ttk.Style(self)
        self.style.configure('Overview.TFrame', background="blue")
        self.style.configure('Treeview.TFrame', background="green")
        self.style.configure('TFrame', background="orange")

        # Create a frame on the left side
        self.left_frame = SemesterTreeviewFrame(master=self, style="Treeview.TFrame")
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.place(relx=0, rely=0, width=400, relheight=1)



        # Create the frame in the middle
        self.middle_frame = CourseOverviewFrame(self, style="Overview.TFrame")
        self.middle_frame.pack(fill="both", expand=True, padx=(410, 10))



class SemesterTreeviewFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Create Header
        self.header = ttk.Label(master=self, text="Studienübersicht")
        self.header.pack(side="top", pady=5)

        # Create a Treeview widget in the left frame
        self.treeview = SemesterTreeview(self, columns=("Durchschnitt",), show="tree")
        self.treeview.column("#0", width=350)
        self.treeview.column("#1", width=50)
        self.treeview.pack(fill="both", expand=True)

    def create_tree_view_from_model(self, user: User):

        self.treeview.insert("", "end", "root_node", text=user.degree_program.name)

        for semester_num, semester in enumerate(user.degree_program.semesters, start=1):
            # Insert the semester node under the root node
            semester_node = self.treeview.insert("root_node", "end", text=f"Semester {semester_num}")

            # Iterate over each course in the semester
            for course in semester.courses:
                # Insert the course node under the semester node
                self.treeview.insert(semester_node, "end", text=course.name, values=(course.exam.grade,))

    def add_treeview_nodes(self):
        # Add the top node "Semester" and its sub-nodes "Semester 1" and "Semester 2"
        self.treeview.insert("", "end", "root_node", text="Semester")
        self.treeview.insert("root_node", iid="semester_1", index="end", text="Semester 1", values=("2",))
        self.treeview.insert("root_node", iid="semester_2", index="end", text="Semester 2", values=("2",))
        self.treeview.insert("root_node", iid="semester_3", index="end", text="Semester 3", values=("2",))
        self.treeview.insert("root_node", iid="semester_4", index="end", text="Semester 4", values=("2",))
        self.treeview.insert("root_node", iid="semester_5", index="end", text="Semester 5", values=("2",))
        self.treeview.insert("root_node", iid="semester_6", index="end", text="Semester 6", values=("2",))

        # Add demo nodes under "Semester 1"
        self.treeview.insert("semester_1", "end", text="Subject A", values=("A+",))
        self.treeview.insert("semester_1", "end", text="Subject B", values=("A",))
        self.treeview.insert("semester_1", "end", text="Subject C", values=("B",))

        # Add demo nodes under "Semester 2"
        self.treeview.insert("semester_2", "end", text="Subject X", values=("B",))
        self.treeview.insert("semester_2", "end", text="Subject Y", values=("C",))
        self.treeview.insert("semester_2", "end", text="Subject Z", values=("A",))

        # Configure tag to set background color for value "B"
        self.treeview.tag_configure("bg_B", background="yellow")

        # Apply the tag to the cell with value "B"
        for child in self.treeview.get_children("semester_2"):
            values = self.treeview.item(child)["values"]
            if values and values[0] == "B":
                self.treeview.item(child, tags=("bg_B",))

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
            color = self.__get_grade_color(kwargs['values'][0])
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


class CourseOverviewFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Course frame containing course name and course ID labels
        self.course_frame = ttk.Frame(self)
        self.course_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Course name label
        self.course_name_label = ttk.Label(self.course_frame, text="course_name", font=("Arial", 16, "bold"))
        self.course_name_label.grid(row=0, column=0, sticky="ew")

        # Course ID label
        self.course_id_label = ttk.Label(self.course_frame, text=f"Course ID: {"course_id"}", font=("Arial", 12))
        self.course_id_label.grid(row=1, column=0, sticky="w")

        # Exam details frame
        self.exam_frame = ttk.Frame(self)
        ttk.Label(self.exam_frame, text="Exam Details").grid(row=0, column=0, sticky="w")
        ttk.Label(self.exam_frame, text="exam_details").grid(row=1, column=0, sticky="w")
        self.exam_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Instructor details frame
        self.instructor_frame = ttk.Frame(self)
        ttk.Label(self.instructor_frame, text="Instructor").grid(row=0, column=0, sticky="w")
        ttk.Label(self.instructor_frame, text="instructor_name").grid(row=1, column=0, sticky="w")
        self.instructor_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Buttons frame (for edit and save buttons)
        self.buttons_frame = ttk.Frame(self)

        # Edit button
        self.edit_button = ttk.Button(self.buttons_frame, text="Edit")
        self.edit_button.grid(row=0, column=0, padx=(0, 5))

        # Save button
        self.save_button = ttk.Button(self.buttons_frame, text="Save")
        self.save_button.grid(row=0, column=1)

        self.buttons_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        # Configure row and column weights
        self.grid_rowconfigure(0, weight=1, uniform="row_weight")
        self.grid_rowconfigure(1, weight=1, uniform="row_weight")
        self.grid_rowconfigure(2, weight=1, uniform="row_weight")
        self.grid_rowconfigure(3, weight=1, uniform="row_weight")
        self.grid_columnconfigure(0, weight=1)

