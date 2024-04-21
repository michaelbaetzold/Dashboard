from controllers import *


class App:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.controller = Controller(self.model, self.view)


if __name__ == "__main__":
    app = App()
