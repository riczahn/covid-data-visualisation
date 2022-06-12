import tkinter as tk
from tkinter import ttk


def print_something():
    print('callback executed')


class Sidebar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.buttons = []

        available_graphs = controller.get_all_graphs()
        self.combo_box = ttk.Combobox(self, values=available_graphs, state='readonly')
        self.combo_box.set(controller.get_current_graph())
        self.combo_box.bind("<<ComboboxSelected>>", self.handle_change)
        self.combo_box.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH)

        lockdowns_button = tk.Button(master=self, text="Show Lockdowns", command=print_something)
        self.buttons.append(lockdowns_button)

        for b in self.buttons:
            b.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH)

    def handle_change(self, event):
        self.controller.show_frame(self.combo_box.get())
