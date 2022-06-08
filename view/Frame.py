import tkinter as tk

from matplotlib.figure import Figure

from view.Graph import Graph
from view.Sidebar import Sidebar


class Frame(tk.Frame):

    def __init__(self, parent, controller, figure: Figure):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.graph = Graph(self, figure)
        self.sidebar = Sidebar(self, controller)

        self.graph.pack()
        self.sidebar.pack()
