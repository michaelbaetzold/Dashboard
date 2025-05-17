from views import *
from models import *
import sys


class Controller:
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.left_frame.treeview.update_grade_list(self.__model.user.grade_goals)
        self.create_tree_view_from_model(self.__model.get_degree_program())
        self.__view.left_frame.treeview.bind("<<TreeviewSelect>>", self.on_semester_treeview_click)
        self.__view.switch("degree")
        self.handle_update_degree_view("this string is irrelevant", "this as well")
        self.__view.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.__view.start_mainloop()


    def create_tree_view_from_model(self, degree_program: DegreeProgram):
        treeview = self.__view.left_frame.treeview
        treeview.delete(*treeview.get_children())
        treeview.insert("", "end", "root_node", text=degree_program.name, values=("", "degree"))
        for semester_num, semester in enumerate(degree_program.semesters, start=1):

            semester_node = treeview.insert(
                "root_node",
                "end", text=semester.name,
                values=("{:.2f}".format(semester.semester_average), "semester"))

            for course in semester.courses:
                treeview.insert(
                    semester_node,
                    "end",
                    text=course.name,
                    values=("{:.2f}".format(course.exam.grade), "course"))

            treeview.insert(
                semester_node,
                "end",
                text="Kurs hinzufügen",
                values=("", "add_course"))

        treeview.insert(
            "root_node",
            "end",
            text="Semester hinzufügen",
            values=("", "add_semester"))

    def on_semester_treeview_click(self, event):
        item_id = event.widget.focus()
        if not item_id:
            return
        view_name = self.__view.left_frame.treeview.item(item_id, "values")[1]
        item_name = event.widget.item(item_id)["text"]
        if not "add_" in view_name:
            self.__view.switch(view_name)

        switch_cases = {
            "course": self.handle_update_course_view,
            "degree": self.handle_update_degree_view,
            "semester": self.handle_update_semester_view,
            "add_semester": self.handle_add_semester,
            "add_course": self.handle_add_course,
        }
        switch_cases.get(view_name, lambda: print("Unknown view"))(item_name, item_id)

    def handle_add_semester(self, item_name, item_id):
        semester_name = self.__model.get_next_semester_name()
        self.__view.left_frame.treeview.add_semester_node(semester_name=semester_name, item_id=item_id)
        self.__model.user.degree_program.semesters.append(Semester(semester_name, list(), 0.0))

    def handle_add_course(self, item_name, item_id):
        course = Course(
            course_id="",
            name="Neuer Kurs",
            ects=5,
            exam= Exam(
                exam_type=ExamTypes.WRITTEN_EXAM,
                attempt=1,
                grade=0.00,
                part_of_final_grade=True
            )
        )
        semester_name = self.__view.left_frame.treeview.add_course_node(item_id, course.name)
        semester = self.__model.get_semester_from_name(semester_name)
        semester.courses.append(course)

    def handle_delete_course(self, event):
        self.handle_save_course_details(event)  # In case the fields were edited beforehand
        course_name = self.__view.central_frame.course_name_var.get()
        treeview_id = self.__view.left_frame.treeview.get_id_from_name(course_name)
        self.__view.left_frame.treeview.delete(treeview_id)
        self.__view.left_frame.treeview.update()

        course = self.__model.get_course_from_name(course_name)
        for semester in self.__model.user.degree_program.semesters:
            if course in semester.courses:
                index = semester.courses.index(course)
                del semester.courses[index]
                break

    def handle_delete_semester(self, event):
        semester_name = self.__view.central_frame.semester_name_var.get()
        treeview_id = self.__view.left_frame.treeview.get_id_from_name(semester_name)
        self.__view.left_frame.treeview.delete(treeview_id)
        self.__view.left_frame.treeview.update()

        semester = self.__model.get_semester_from_name(semester_name)
        semesters = self.__model.user.degree_program.semesters
        if semester in semesters:
            index = semesters.index(semester)
            del semesters[index]


    def handle_update_course_view(self, item_name, item_id):
        self.__view.central_frame.update_view_from_model(self.__model.get_course_from_name(item_name))
        self.__view.central_frame.button.bind("<Button-1>", self.handle_save_course_details)
        self.__view.central_frame.button_del.bind("<Button-1>", self.handle_delete_course)

    def handle_update_degree_view(self, item_name, item_id):
        self.__view.central_frame.update_view_from_model(self.__model.get_degree_program())

    def handle_update_semester_view(self, item_name, item_id):
        self.__view.central_frame.update_view_from_model(self.__model.get_semester_from_name(item_name))
        self.__view.central_frame.button_del.bind("<Button-1>", self.handle_delete_semester)

    def handle_save_course_details(self, event):
        course = Course(
            course_id=self.__view.central_frame.course_id_var.get(),
            ects=self.__view.central_frame.ects_var.get(),
            name=self.__view.central_frame.course_name_var.get(),
            exam=Exam(
                exam_type=ExamTypes.get_exam_type(self.__view.central_frame.exam_details_var.get()),
                attempt=self.__view.central_frame.attempt_var.get(),
                grade=self.__view.central_frame.grade_var.get(),
                part_of_final_grade=self.__view.central_frame.part_of_final_grade_var.get()
            )
        )
        indices = self.__view.left_frame.treeview.get_focussed_indices()
        self.__model.update_course_model_from_view(course, indices)

        # Update the semester treeview
        treeview = self.__view.left_frame.treeview
        selection = treeview.selection()
        if selection:
            index = treeview.index(selection)
            parent = treeview.parent(selection)
            treeview.delete(selection)
            if parent:
                selection = treeview.insert(
                    parent,
                    index,
                    text=course.name,
                    values=("{:.2f}".format(course.exam.grade), "course"))
                # Update semester tree average
                semester_values = treeview.item(parent, "values")
                semester_name = treeview.item(parent, "text")
                semester = self.__model.get_semester_from_name(semester_name)
                new_semester_average = semester.update_semester_average()
                new_semester_values = ("{:.2f}".format(new_semester_average), semester_values[1])
                treeview.item(parent, values=new_semester_values)
                treeview.selection_add(selection)
                treeview.focus(selection)

            else:
                print("Error at treeview update")

    def on_close(self):
        self.__model.save_data_to_json()
        sys.exit()

