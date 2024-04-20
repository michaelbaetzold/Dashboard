import tkinter as tk
from tkinter import ttk

import Views.view
from Views.view import *

import Models.model
from Models.model import *

import Controllers.controllers
from Controllers.controllers import *

class App:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.controller = Controller(self.model, self.view)

if __name__ == "__main__":
    app = App()
