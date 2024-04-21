import Views.view
from Views.view import *
import Models.model
from Models.model import *
import sys


class Controller:
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view
        self.__view.left_frame.create_tree_view_from_model(self.__model.get_degree_program())
        self.__view.left_frame.treeview.bind("<<TreeviewSelect>>", self.on_semester_treeview_click)
        self.__view.switch("degree")
        self.handle_update_degree_view("this string is irrelevant")
        self.__view.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.__view.start_mainloop()

    def on_semester_treeview_click(self, event):
        item_id = event.widget.focus()
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
        print("asd")

    def on_close(self):
        self.__model.save_data_to_json()
        sys.exit()

