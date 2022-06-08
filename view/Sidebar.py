import tkinter as tk


class Sidebar:

    def __init__(self, root, controller):
        self.root = root
        self.buttons = []

        button = tk.Button(master=self.root, text="Change", command=controller.next_graph)
        self.buttons.append(button)

    def pack(self):
        for button in self.buttons:
            button.pack(side=tk.RIGHT, anchor=tk.W)
