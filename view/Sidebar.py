import tkinter as tk

from view.Graph import Graph


class Sidebar:

    def __init__(self, root, graph: Graph):
        self.root = root
        self.buttons = []
        self.graph = graph
        self.draw()

    def draw(self):
        button = tk.Button(master=self.root, text="Change", command=self.graph.load_data)
        self.buttons.append(button)

    def pack(self):
        for button in self.buttons:
            button.pack(side=tk.RIGHT, anchor=tk.W)
