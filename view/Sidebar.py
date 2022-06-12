import tkinter as tk


def print_something():
    print('callback executed')


class Sidebar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.buttons = []

        next_graph_button = tk.Button(master=self, text="Next Graph", command=controller.next_graph)
        self.buttons.append(next_graph_button)

        lockdowns_button = tk.Button(master=self, text="Show Lockdowns", command=print_something)
        self.buttons.append(lockdowns_button)

        for b in self.buttons:
            b.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH)

