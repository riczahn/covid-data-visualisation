import tkinter as tk

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Graph:
    def __init__(self, parent, figure: Figure):
        self.root = parent

        self.canvas = FigureCanvasTkAgg(figure, master=parent)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

        self.canvas.mpl_connect("key_press_event", self.on_key_press)

    def pack(self):
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
