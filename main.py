import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self):
        self.BuildGui()
        # Run the main event loop
        self.window.mainloop()

    def LoadUserSettings(self):
        #placeholder
        print("test")

    def BuildGui(self):
        # Initialize the tkinter root window
        self.window = tk.Tk()
        self.window.title("Dashboard")
        self.window.geometry("1000x600")
        self.window.minsize(500, 300)

        # Configure the style for the entire application
        self.style = ttk.Style(self.window)
        self.style.configure('Overview.TFrame', background="blue")
        self.style.configure('Treeview.TFrame', background="green")

        # Create a frame on the left side
        self.left_frame = ttk.Frame(self.window, style="Treeview.TFrame")
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.place(relx=0, rely=0, width=200, relheight=1)

        # Create the frame in the middle
        self.middle_frame = ttk.Frame(self.window, style="Overview.TFrame")
        self.middle_frame.pack(fill="both", expand=True, padx=(210, 10))
        # self.middle_frame.place(x=210, rely=0, relheight=1)

        # Create a Treeview widget in the left frame
        self.treeview = ttk.Treeview(self.left_frame, columns="Durchschnitt")
        self.treeview.column("#0", width=150)
        self.treeview.column("#1", width=50)
        self.treeview.pack(fill="both", expand=True)

        # Add the top node "Semester" and its sub-nodes "Semester 1" and "Semester 2"
        self.treeview.insert("", "end", "root_node", text="Semester")
        self.treeview.insert("root_node", "end", text="Semester 1", values="2")
        self.treeview.insert("root_node", "end", text="Semester 2", values="2")
        self.treeview.insert("root_node", "end", text="Semester 3", values="2")
        self.treeview.insert("root_node", "end", text="Semester 4", values="2")
        self.treeview.insert("root_node", "end", text="Semester 5", values="2")
        self.treeview.insert("root_node", "end", text="Semester 6", values="2")

    def FillTreeviewFromCSV(self):
        #placeholder
        print("test")

if __name__ == "__main__":
    app = App()
