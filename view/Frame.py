import tkinter as tk

from matplotlib.figure import Figure

from view.Graph import Graph


class Frame(tk.Frame):

    def __init__(self, parent, figure: Figure):
        tk.Frame.__init__(self, parent)
        self.graph = Graph(self, figure)

        self.graph.grid(row=0, column=0, sticky="n")

