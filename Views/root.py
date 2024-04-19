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

        # Create a frame on the left side
        self.left_frame = SemesterTreeviewFrame(master=self, style="Treeview.TFrame")
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.place(relx=0, rely=0, width=400, relheight=1)



        # Create the frame in the middle
        self.middle_frame = ttk.Frame(self, style="Overview.TFrame")
        self.middle_frame.pack(fill="both", expand=True, padx=(410, 10))
        # self.middle_frame.place(x=210, rely=0, relheight=1)


class SemesterTreeviewFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Create Header
        self.header = ttk.Label(master=self, text="Studienübersicht")
        self.header.pack(side="top", pady=5)

        # Create a Treeview widget in the left frame
        self.treeview = ttk.Treeview(self, columns=("Durchschnitt",), show="tree")
        self.treeview.column("#0", width=350)
        self.treeview.column("#1", width=50)
        self.treeview.pack(fill="both", expand=True)

        #self.addTreeviewNodes()

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

