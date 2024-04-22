from views import *
from models import *
import sys


class Controller:
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.left_frame.treeview.update_grade_list(self.__model.user.grade_goals)
        self.__view.left_frame.create_tree_view_from_model(self.__model.get_degree_program())
        self.__view.left_frame.treeview.bind("<<TreeviewSelect>>", self.on_semester_treeview_click)
        self.__view.switch("degree")
        self.handle_update_degree_view("this string is irrelevant")
        self.__view.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.__view.start_mainloop()

    def on_semester_treeview_click(self, event):
        item_id = event.widget.focus()
        if not item_id:  # see handle_save_course_details
            return
        view_name = self.__view.left_frame.treeview.item(item_id, "values")[1]
        item_name = event.widget.item(item_id)["text"]
        self.__view.switch(view_name)

        switch_cases = {
            "course": self.handle_update_course_view,
            "degree": self.handle_update_degree_view,
            "semester": self.handle_update_semester_view,
        }
        switch_cases.get(view_name, lambda: print("Unknown view"))(item_name)

    def handle_update_course_view(self, item_name):
        self.__view.central_frame.update_view_from_model(self.__model.get_course_from_name(item_name))
        self.__view.central_frame.button.bind("<Button-1>", self.handle_save_course_details)

    def handle_update_degree_view(self, item_name):
        self.__view.central_frame.update_view_from_model(self.__model.get_degree_program())

    def handle_update_semester_view(self, item_name):
        self.__view.central_frame.update_view_from_model(self.__model.get_semester_from_name(item_name))

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
        self.__model.update_course_model_from_view(course)

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

                # treeview.update()
                treeview.focus(selection)
                # TODO debug and fix
                # There is a problem with the select method. It raises the <<TreeviewSelect>>
                # event, which triggers the on_semester_treeview_click method
                # however the event doesn't have the x, y, coordinates and therefore finds no
                # node and can't access the values tuple and throws an error.

            else:
                print("Error at treeview update")

    def on_close(self):
        self.__model.save_data_to_json()
        sys.exit()

