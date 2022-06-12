import tkinter as tk

from matplotlib.figure import Figure

from view.Graph import Graph
from view.Sidebar import Sidebar


class Frame(tk.Frame):

    def __init__(self, parent, controller, figure: Figure):
        tk.Frame.__init__(self, parent)
        self.graph = Graph(self, figure)
        self.sidebar = Sidebar(self, controller)

        self.graph.grid(row=0, column=0, sticky="n")
        self.sidebar.grid(row=0, column=1, sticky="n")

